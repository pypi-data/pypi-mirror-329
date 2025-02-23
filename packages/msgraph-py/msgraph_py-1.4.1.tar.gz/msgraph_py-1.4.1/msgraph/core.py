import atexit
import logging
import uuid
from base64 import urlsafe_b64encode
from binascii import unhexlify
from getpass import getpass
from os import environ
from pathlib import Path
from time import time
from typing import Union
from urllib.parse import quote_plus

import httpx
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    pkcs12,
)
from cryptography.x509 import Certificate, load_pem_x509_certificate

logger = logging.getLogger(__name__)
_http_client = None
_token_cache = {}

DEFAULT_TIMEOUT = 30.0


def ensure_list(value: Union[list[str], str]) -> list[str]:
    """
    Helper function that always returns a string as a list[str].

    """

    return [value] if isinstance(value, str) else value


def filter_none(dictionary: dict) -> dict:
    """
    Helper function to filter out None values from dictionaries.
    This is necessary as part of building params and header
    dictionaries for httpx requests, as None values cause issues
    with encoding internally in httpx.

    """

    filtered_dict = {}
    for key, value in dictionary.items():
        if value is not None:
            filtered_dict[key] = value
    return filtered_dict


def get_http_client() -> httpx.Client:
    """
    Returns a new or existing HTTP client and sets it as a global
    variable, enabling connection pooling and HTTP/2 support.

    """

    global _http_client
    if _http_client is None:
        logger.info("Initializing new HTTP client ..")
        _http_client = httpx.Client(http2=True, timeout=DEFAULT_TIMEOUT)
    else:
        logger.info("Using existing HTTP client")
    return _http_client


def get_token() -> str:
    """
    Returns an access token for the client in Azure AD.
    Uses the same token from _token_cache in repeated API-calls.

    Documentation:
    https://learn.microsoft.com/en-us/graph/auth/auth-concepts

    """

    BASE_URL = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"
    CLOCK_SKEW_SECONDS = 5 * 60

    global _token_cache
    if _token_cache:
        if _token_cache["exp"] >= time() + CLOCK_SKEW_SECONDS:
            logger.info("Using cached access token")
            return _token_cache["jwt"]
        else:
            logger.info("Cached access token has expired")

    (
        tenant_id,
        client_id,
        client_secret,
        key_path,
        key_passphrase,
        thumbprint,
    ) = _get_config()

    url = BASE_URL.format(quote_plus(tenant_id))
    payload = {
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default",
        "client_id": client_id,
    }

    if client_secret:
        logger.info("Using client_secret to authenticate the client")
        payload["client_secret"] = client_secret

    elif key_path:
        logger.info("Using client_assertion to authenticate the client")

        if not thumbprint:
            logger.debug("No thumbprint provided. Will attempt to load certificate")
            key, cert = _get_key_and_cert(key_path, key_passphrase, include_cert=True)
            thumbprint = cert.fingerprint(hashes.SHA256()).hex()
        else:
            key, _ = _get_key_and_cert(key_path, key_passphrase)
        logger.debug(f"Thumbprint: {thumbprint}")

        assertion_type = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
        jwt_assertion = _get_jwt_assertion(client_id, url, key, thumbprint)

        payload["client_assertion_type"] = assertion_type
        payload["client_assertion"] = jwt_assertion

    else:
        raise ValueError(
            "Unknown client authentication method. No client_secret or key_path provided."
        )

    logger.info("Getting access token ..")

    client = get_http_client()
    response = client.post(url, data=payload)

    if response.status_code != 200:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason_phrase,
            response.json().get("error_description"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    data = response.json()
    _token_cache["jwt"] = data["access_token"]
    _token_cache["exp"] = time() + data["expires_in"]

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
    logger.info(f"Access token retrieved and saved to cache ({seconds_str})")

    return data["access_token"]


def _get_config() -> tuple[str]:
    """
    Returns a tuple with variables for connecting to the Azure AD client.

    Attempts to read AAD_TENANT_ID, AAD_CLIENT_ID and AAD_CLIENT_SECRET
    from settings.py when running from Django, or alternatively from os.environ
    if Django is not installed or settings are not initialized.

    Prompts the user for input if any of the required variables are empty.

    """

    try:
        from django.conf import settings

        # If settings.py is initialized
        if settings.configured:
            logger.info("Importing client credentials from django.conf.settings")
            tenant_id = settings.AAD_TENANT_ID
            client_id = settings.AAD_CLIENT_ID
            client_secret = settings.AAD_CLIENT_SECRET
            key_path = settings.AAD_PRIVATE_KEY_PATH
            key_passphrase = settings.AAD_PRIVATE_KEY_PASSPHRASE
            thumbprint = settings.AAD_CERT_THUMBPRINT
        else:
            raise ImportError("Django not running")

    # Django is not installed or not running
    except ImportError:
        logger.info("Importing client credentials from os.environ")
        tenant_id = environ.get("AAD_TENANT_ID")
        client_id = environ.get("AAD_CLIENT_ID")
        client_secret = environ.get("AAD_CLIENT_SECRET")
        key_path = environ.get("AAD_PRIVATE_KEY_PATH")
        key_passphrase = environ.get("AAD_PRIVATE_KEY_PASSPHRASE")
        thumbprint = environ.get("AAD_CERT_THUMBPRINT")

    if client_secret and key_path:
        raise ValueError(
            "Ambiguous client authentication method. AAD_CLIENT_SECRET and AAD_PRIVATE_KEY_PATH are mutually exclusive."
        )
    elif any([key_passphrase, thumbprint]) and not key_path:
        logger.warning(
            "AAD_PRIVATE_KEY_PATH is not set. AAD_PRIVATE_KEY_PASSPHRASE and AAD_CERT_THUMBPRINT variables will be ignored."
        )

    if not tenant_id:
        logger.info("AAD_TENANT_ID missing or empty")
        tenant_id = input("AAD_TENANT_ID: ")
    if not client_id:
        logger.info("AAD_CLIENT_ID missing or empty")
        client_id = input("AAD_CLIENT_ID: ")
    if not client_secret and not key_path:
        logger.info("AAD_CLIENT_SECRET and AAD_PRIVATE_KEY_PATH missing or empty")
        client_secret = getpass("AAD_CLIENT_SECRET: ")

    return (
        tenant_id,
        client_id,
        client_secret,
        key_path,
        key_passphrase,
        thumbprint,
    )


def _get_jwt_assertion(
    issuer: str,
    audience: str,
    key: PrivateKeyTypes,
    thumbprint: str,
    expires_in: int = 30,
) -> str:
    """
    Returns a signed JWT for use in client authentication.

    The issuer parameter must be the client ID of the app in Entra ID.
    The audience parameter must be the URL of the tenant's token endpoint.
    The thumbprint parameter must be either a SHA-1 or SHA-256 thumbprint
    of the certificate uploaded to the clients app registration in Entra ID.

    The expires_in parameter defaults to 30 seconds and is added to the exp
    claim in the JWT, expressing the epoch time when the JWT will expire.
    This value should be kept reasonably short.

    Documentation:
    https://learn.microsoft.com/en-us/entra/identity-platform/certificate-credentials

    """

    headers = {}
    encoded_thumbprint = urlsafe_b64encode(unhexlify(thumbprint)).rstrip(b"=").decode()

    if len(thumbprint) == 40:
        headers["x5t"] = encoded_thumbprint
    elif len(thumbprint) == 64:
        headers["x5t#S256"] = encoded_thumbprint
    else:
        raise ValueError(
            f"Certificate thumbprint {thumbprint} has incorrect length. Must be either 40 (SHA-1) or 64 (SHA-256) characters"
        )

    current_time = int(time())
    claims = {
        "aud": audience,
        "iss": issuer,
        "sub": issuer,
        "iat": current_time,
        "nbf": current_time,
        "exp": current_time + expires_in,
        "jti": str(uuid.uuid4()),
    }
    logger.debug(f"JWT assertion headers: {headers}")
    logger.debug(f"JWT assertion claims: {claims}")

    return jwt.encode(claims, key, algorithm="PS256", headers=headers)


def _get_key_and_cert(
    key_path: str,
    key_passphrase: str = None,
    include_cert: bool = False,
) -> tuple[PrivateKeyTypes, Certificate | None]:
    """
    Returns the private key from the specified key_path and optionally
    the X.509 certificate as a tuple. The include_cert parameter is False
    by default and requires the certificate to be included in the same
    file as the private key.

    The certificate is used to automatically retrieve the thumbprint,
    as this is required for the x5t#S256 header when constructing the
    JWT assertion later. MS Graph uses this as a reference to the
    certificate uploaded to the clients app registration in Entra ID.

    Currently only supports PKCS#12 and PEM formats.

    """

    with open(key_path, "rb") as f:
        logger.debug(f"Reading key_bytes from {key_path}")
        key_bytes = f.read()

    encoded_passphrase = key_passphrase.encode() if key_passphrase else None

    # Checks the file extension to determine if the key is in PKCS#12 format
    if Path(key_path).suffix in [".pfx", ".p12"]:
        logger.debug("Using PKCS#12 format to load the private key")
        key, cert, _ = pkcs12.load_key_and_certificates(key_bytes, encoded_passphrase)

    # Assumes PEM format otherwise
    else:
        logger.debug("Using PEM format to load the private key")
        key = load_pem_private_key(key_bytes, encoded_passphrase)

        if include_cert:
            cert = load_pem_x509_certificate(key_bytes)

    return (key, cert) if include_cert else (key, None)


@atexit.register
def exit_handler():
    """
    Ensures the HTTP client is always closed when the application
    terminates execution.

    """

    global _http_client
    if _http_client is not None:
        logger.info("Closing HTTP client ..")
        _http_client.close()
        _http_client = None
