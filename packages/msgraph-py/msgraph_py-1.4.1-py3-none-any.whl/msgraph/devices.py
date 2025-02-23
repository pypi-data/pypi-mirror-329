import logging
from base64 import b64decode
from typing import Union
from urllib.parse import quote_plus, urljoin

from .core import DEFAULT_TIMEOUT, ensure_list, filter_none, get_http_client, get_token

logger = logging.getLogger(__name__)


def get_device(
    device_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> Union[list[dict], dict]:
    """
    Returns one or more devices from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "Device.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/device
    https://learn.microsoft.com/en-us/graph/api/device-list

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/devices"
    MAX_PAGE_SIZE = 999

    if device_id and (filter or search):
        raise ValueError(
            "Parameters device_id and filter|search are mutually exclusive."
        )

    url = urljoin(f"{BASE_URL}/", quote_plus(device_id)) if device_id else BASE_URL
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
    logger.info("Getting devices ..")

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

    return data[0] if device_id else data


def delete_device(device_id: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
    """
    Deletes a device based on its id property.

    Requires admin consent for "Device.ReadWrite.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/device-delete

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/devices/{}"

    url = BASE_URL.format(quote_plus(device_id))
    headers = {"Authorization": f"Bearer {get_token()}"}

    logger.info(f"Deleting device {device_id} ..")

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


def list_owned_devices(
    user_id: str,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[dict]:
    """
    Returns a list of devices owned by a user from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "Directory.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/user-list-owneddevices

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/users/{}/ownedDevices"
    MAX_PAGE_SIZE = 999

    url = BASE_URL.format(quote_plus(user_id))
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
    logger.info(f"Getting devices owned by {user_id} ..")

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

        data.extend(response.json().get("value"))
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

    return data


def get_laps_password(
    device_id: str, timeout: float = DEFAULT_TIMEOUT
) -> Union[str, None]:
    """
    Returns a string with the current decoded LAPS password for an
    Intune device from the Microsoft Graph API. Returns None if the
    response is empty (no LAPS password).

    Requires admin consent for "DeviceLocalCredential.Read.All" app
    permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/devicelocalcredentialinfo
    https://learn.microsoft.com/en-us/graph/api/devicelocalcredentialinfo-get

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/directory/deviceLocalCredentials/{}"

    url = BASE_URL.format(quote_plus(device_id))
    headers = {"Authorization": f"Bearer {get_token()}"}
    params = {"$select": "credentials"}

    logger.info(f"Getting LAPS password for {device_id} ..")

    client = get_http_client()
    response = client.get(url, headers=headers, params=params, timeout=timeout)

    if response.status_code != 200:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason_phrase,
            response.json().get("error", {}).get("message"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())

    if "application/json" not in response.headers.get("Content-Type", ""):
        logger.warning(f"Device {device_id} has no LAPS passwords ({seconds_str})")
        return None

    data = response.json()["credentials"]

    encoded_pwd = data[0].get("passwordBase64", "")
    decoded_pwd = b64decode(encoded_pwd).decode("utf-8")

    logger.info(f"Received {len(data)} objects ({seconds_str})")

    return decoded_pwd


def get_bitlocker_key(
    key_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> Union[list[dict], dict]:
    """
    Returns one or more BitLocker recovery key objects from the
    Microsoft Graph API. To retrieve the actual recovery key, use
    the select="key" parameter combined with key_id.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Requires admin consent for "BitlockerKey.Read.All" app
    permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/bitlockerrecoverykey
    https://learn.microsoft.com/en-us/graph/api/bitlocker-list-recoverykeys
    https://learn.microsoft.com/en-us/graph/api/bitlockerrecoverykey-get

    """

    BASE_URL = (
        "https://graph.microsoft.com/v1.0/informationProtection/bitlocker/recoveryKeys"
    )
    MAX_PAGE_SIZE = 999  # Unknown

    if key_id and (filter or search):
        raise ValueError("Parameters key_id and filter|search are mutually exclusive.")

    url = urljoin(f"{BASE_URL}/", quote_plus(key_id)) if key_id else BASE_URL
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
    params = filter_none(params)
    headers = filter_none(headers)

    data = []
    count = -1
    total_seconds = 0.0
    logger.info("Getting BitLocker keys ..")

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

    return data[0] if key_id else data


def get_device_bitlocker_key(
    device_id: str, timeout: float = DEFAULT_TIMEOUT
) -> list[dict]:
    """
    Convenience function to get BitLocker recovery keys based on deviceId
    alone. Performs at least two API requests using get_bitlocker_key(),
    one to get the BitLocker key ID and one to get the actual recovery key,
    as the key ID is needed before requesting the recovery key. This is
    likely due to the select=key query parameter triggering an audit log
    of the operation in Microsoft Entra.

    Requires admin consent for "BitlockerKey.Read.All" app permissions in
    the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/bitlockerrecoverykey

    """

    device_bitlocker_keys = []

    for key in get_bitlocker_key(filter=f"deviceId eq '{device_id}'", timeout=timeout):
        bitlocker_key = get_bitlocker_key(
            key_id=key["id"], select="key", timeout=timeout
        )
        device_bitlocker_keys.append(bitlocker_key)

    return device_bitlocker_keys
