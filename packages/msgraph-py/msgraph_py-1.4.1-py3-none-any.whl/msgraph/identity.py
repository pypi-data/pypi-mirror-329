import logging
from typing import Union
from urllib.parse import quote_plus, urljoin

from .core import DEFAULT_TIMEOUT, ensure_list, filter_none, get_http_client, get_token

logger = logging.getLogger(__name__)


def get_user(
    user_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> Union[list[dict], dict]:
    """
    Returns one or more users from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "User.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/user
    https://learn.microsoft.com/en-us/graph/api/user-list

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/users"
    MAX_PAGE_SIZE = 999

    if user_id and (filter or search):
        raise ValueError("Parameters user_id and filter|search are mutually exclusive.")

    url = urljoin(f"{BASE_URL}/", quote_plus(user_id)) if user_id else BASE_URL
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "ConsistencyLevel": "eventual" if filter or search or orderby else None,
    }
    params = {
        "$select": ",".join(ensure_list(select)) if select else None,
        "$filter": filter,
        "$search": f'"{search}"' if search else None,
        "$orderby": ",".join(ensure_list(orderby)) if orderby else None,
        "$top": top if top is not None else (MAX_PAGE_SIZE if all else None),
        "$count": "true" if filter or search or orderby else None,
    }
    headers = filter_none(headers)
    params = filter_none(params)

    data = []
    count = -1
    total_seconds = 0.0
    logger.info("Getting users ..")

    client = get_http_client()

    while True:
        response = client.get(url, headers=headers, params=params, timeout=timeout)
        total_seconds += response.elapsed.total_seconds()

        if response.status_code != 200:
            error_message = "Request failed ({} {}) - {}".format(
                response.status_code,
                response.reason_phrase,
                response.json().get("error", {}).get("message"),
            )
            logger.error(error_message)
            raise ConnectionError(error_message)

        data.extend(response.json().get("value", [response.json()]))
        next_link = response.json().get("@odata.nextLink")

        if next_link and (all and top is None):
            if "@odata.count" in response.json():  # Only returned in the first page
                count = response.json().get("@odata.count")

            seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
            logger.debug(
                f"Received {len(data)}/{count} objects in response ({seconds_str})"
            )

            params["$skiptoken"] = next_link.split("$skiptoken=")[1]
        else:
            break

    total_seconds_str = "{:.1f} s".format(total_seconds)
    logger.info(f"Received {len(data)} objects ({total_seconds_str})")

    return data[0] if user_id else data


def revoke_refresh_tokens(user_id: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
    """
    Revokes all refresh tokens for a given user.

    Requires admin consent for "User.ReadWrite.All" app permissions.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/user-revokesigninsessions

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/users/{}/revokeSignInSessions"

    url = BASE_URL.format(quote_plus(user_id))
    headers = {"Authorization": f"Bearer {get_token()}"}

    logger.info(f"Revoking refresh tokens for {user_id} ..")

    client = get_http_client()
    response = client.post(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason_phrase,
            response.json().get("error", {}).get("message"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
    logger.info(f"Request completed successfully {seconds_str}")

    return response.json()["value"]


def list_auth_methods(user_id: str, timeout: float = DEFAULT_TIMEOUT) -> list[dict]:
    """
    Returns a list of all authentication methods for a given user.

    Requires admin consent for "UserAuthenticationMethod.Read.All" app permissions.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/authentication-list-methods

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/users/{}/authentication/methods"

    url = BASE_URL.format(quote_plus(user_id))
    headers = {"Authorization": f"Bearer {get_token()}"}

    logger.info(f"Getting authentication methods for {user_id} ..")

    client = get_http_client()
    response = client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason_phrase,
            response.json().get("error", {}).get("message"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    data = response.json()["value"]

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
    logger.info(f"Received {len(data)} objects ({seconds_str})")

    return data


def delete_auth_method(
    user_id: str, auth_method: dict, timeout: float = DEFAULT_TIMEOUT
) -> bool:
    """
    Deletes an authentication method for a user and returns True or False.
    Expects a dictionary object in the auth_method parameter from list_auth_methods()
    to find the method's id and @odata.type since each authentication method resides
    in its own endpoint and must be mapped based on its type.

    Requires admin consent for "UserAuthenticationMethod.ReadWrite.All" app permissions.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/users/{}/authentication/{}/{}"

    method_id = auth_method["id"]
    method_type = auth_method["@odata.type"].replace("#microsoft.graph.", "")

    if method_type == "microsoftAuthenticatorAuthenticationMethod":
        endpoint = "microsoftAuthenticatorMethods"
    elif method_type == "phoneAuthenticationMethod":
        endpoint = "phoneMethods"
    elif method_type == "softwareOathAuthenticationMethod":
        endpoint = "softwareOathMethods"
    elif method_type == "fido2AuthenticationMethod":
        endpoint = "fido2Methods"
    elif method_type == "windowsHelloForBusinessAuthenticationMethod":
        endpoint = "windowsHelloForBusinessMethods"
    elif method_type == "emailAuthenticationMethod":
        endpoint = "emailMethods"
    else:
        logger.info(f"No matching endpoint for type {method_type}")
        return False

    url = BASE_URL.format(quote_plus(user_id), endpoint, quote_plus(method_id))
    headers = {"Authorization": f"Bearer {get_token()}"}

    logger.info(f"Deleting {method_type} {method_id} for user {user_id} ..")

    client = get_http_client()
    response = client.delete(url, headers=headers, timeout=timeout)

    if response.status_code != 204:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason_phrase,
            response.json().get("error", {}).get("message"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
    logger.info(f"Request completed successfully {seconds_str}")

    return True


def reset_strong_auth(user_id: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
    """
    Resets 2FA by deleting the user's registered authentication methods.
    The API has no way to check the default method, which must be deleted last.
    A work-around is to temporarily store the method from the failed request
    and try again after the for-loop.

    Requires admin consent for "UserAuthenticationMethod.ReadWrite.All" and
    "User.ReadWrite.All" app permissions.

    """

    default_method = None

    revoke_refresh_tokens(user_id, timeout=timeout)

    for method in list_auth_methods(user_id, timeout=timeout):
        try:
            delete_auth_method(user_id, method, timeout=timeout)
        except ConnectionError:
            if not default_method:
                default_method = method
                logger.info("Assigned method to default_method")
                continue
            else:
                logger.error("default_method is already assigned")
                raise
    if default_method:
        delete_auth_method(user_id, default_method, timeout=timeout)

    return True


def get_user_risk(
    user_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> Union[list[dict], dict]:
    """
    Returns the user risk status for one or more users from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 20 objects by default.
    This can be specified by setting top=[1..500], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "IdentityRiskyUser.Read.All" app permissions in the
    client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/riskyuser
    https://learn.microsoft.com/en-us/graph/api/riskyuser-list

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/identityProtection/riskyUsers"
    MAX_PAGE_SIZE = 500

    if user_id and (filter or search):
        raise ValueError("Parameters user_id and filter|search are mutually exclusive.")

    url = urljoin(f"{BASE_URL}/", quote_plus(user_id)) if user_id else BASE_URL
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "ConsistencyLevel": "eventual" if filter or search or orderby else None,
    }
    params = {
        "$select": ",".join(ensure_list(select)) if select else None,
        "$filter": filter,
        "$search": f'"{search}"' if search else None,
        "$orderby": ",".join(ensure_list(orderby)) if orderby else None,
        "$top": top if top is not None else (MAX_PAGE_SIZE if all else None),
        "$count": "true" if filter or search or orderby else None,
    }
    headers = filter_none(headers)
    params = filter_none(params)

    data = []
    count = -1
    total_seconds = 0.0
    logger.info("Getting risky users ..")

    client = get_http_client()

    while True:
        response = client.get(url, headers=headers, params=params, timeout=timeout)
        total_seconds += response.elapsed.total_seconds()

        if response.status_code != 200:
            error_message = "Request failed ({} {}) - {}".format(
                response.status_code,
                response.reason_phrase,
                response.json().get("error", {}).get("message"),
            )
            logger.error(error_message)
            raise ConnectionError(error_message)

        data.extend(response.json().get("value", [response.json()]))
        next_link = response.json().get("@odata.nextLink")

        if next_link and (all and top is None):
            if "@odata.count" in response.json():  # Only returned in the first page
                count = response.json().get("@odata.count")

            seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
            logger.debug(
                f"Received {len(data)}/{count} objects in response ({seconds_str})"
            )

            params["$skiptoken"] = next_link.split("$skiptoken=")[1]
        else:
            break

    total_seconds_str = "{:.1f} s".format(total_seconds)
    logger.info(f"Received {len(data)} objects ({total_seconds_str})")

    return data[0] if user_id else data


def get_signin(
    signin_id: str = None,
    filter: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> Union[list[dict], dict]:
    """
    Returns sign-in events for one or more users from the Microsoft Graph API.
    The parameters filter and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 1000 objects by default.
    This can be specified by setting top=[1..1000], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "AuditLog.Read.All" app permissions in the
    client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/signin
    https://learn.microsoft.com/en-us/graph/api/signin-list

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
    MAX_PAGE_SIZE = 1000

    if signin_id and filter:
        raise ValueError("Parameters signin_id and filter are mutually exclusive.")

    url = urljoin(f"{BASE_URL}/", quote_plus(signin_id)) if signin_id else BASE_URL
    headers = {
        "Authorization": f"Bearer {get_token()}",
    }
    params = {
        "$filter": filter,
        "$orderby": ",".join(ensure_list(orderby)) if orderby else None,
        "$top": top if top is not None else (MAX_PAGE_SIZE if all else None),
    }
    params = filter_none(params)

    data = []
    total_seconds = 0.0
    logger.info("Getting sign-ins ..")

    client = get_http_client()

    while True:
        response = client.get(url, headers=headers, params=params, timeout=timeout)
        total_seconds += response.elapsed.total_seconds()

        if response.status_code != 200:
            error_message = "Request failed ({} {}):\n{}".format(
                response.status_code,
                response.reason_phrase,
                response.json().get("error", {}).get("message"),
            )
            logger.error(error_message)
            raise ConnectionError(error_message)

        data.extend(response.json().get("value", [response.json()]))
        next_link = response.json().get("@odata.nextLink")

        if next_link and (all and top is None):
            seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
            logger.debug(f"Received {len(data)} objects in response ({seconds_str})")

            params["$skiptoken"] = next_link.split("$skiptoken=")[1]
        else:
            break

    total_seconds_str = "{:.1f} s".format(total_seconds)
    logger.info(f"Received {len(data)} objects ({total_seconds_str})")

    return data[0] if signin_id else data
