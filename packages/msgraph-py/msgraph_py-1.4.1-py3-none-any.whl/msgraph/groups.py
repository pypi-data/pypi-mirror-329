import logging
from typing import Union
from urllib.parse import quote_plus, urljoin

from .core import DEFAULT_TIMEOUT, ensure_list, filter_none, get_http_client, get_token

logger = logging.getLogger(__name__)


def get_group(
    group_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> Union[list[dict], dict]:
    """
    Returns one or more groups from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "GroupMember.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/group
    https://learn.microsoft.com/en-us/graph/api/group-list

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/groups"
    MAX_PAGE_SIZE = 999

    if group_id and (filter or search):
        raise ValueError(
            "Parameters group_id and filter|search are mutually exclusive."
        )

    url = urljoin(f"{BASE_URL}/", quote_plus(group_id)) if group_id else BASE_URL
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
    logger.info("Getting groups ..")

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

    return data[0] if group_id else data


def list_group_members(
    group_id: str,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[dict]:
    """
    Returns a list of group members from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "GroupMember.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/directoryobject
    https://learn.microsoft.com/en-us/graph/api/group-list-members

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/groups/{}/members"
    MAX_PAGE_SIZE = 999

    url = BASE_URL.format(quote_plus(group_id))
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
    logger.info(f"Getting group {group_id} members ..")

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


def add_group_member(
    group_id: str, members: Union[list[str], str], timeout: float = DEFAULT_TIMEOUT
) -> bool:
    """
    Adds members to a security group or M365 group. Supports adding multiple
    members at once; the function will dynamically split the API-calls in
    batches of 20 members (limit of each API-request).

    Requires admin consent for "GroupMember.ReadWrite.All" app permissions in
    the client, in addition to *.ReadWrite.All for the corresponding resource
    type that's being added (device, group, orgContact, servicePrincipal, user).

    To add members to a role-assignable group, the app must also be assigned
    the "RoleManagement.ReadWrite.Directory" permission.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/group-post-members

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/groups/{}"
    PAYLOAD_URL = "https://graph.microsoft.com/v1.0/directoryObjects/{}"
    MAX_BATCH_SIZE = 20

    url = BASE_URL.format(quote_plus(group_id))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_token()}",
    }

    members = ensure_list(members)
    total_seconds = 0.0
    logger.info(f"Adding {len(members)} members to group {group_id} ..")

    client = get_http_client()

    for i in range(0, len(members), MAX_BATCH_SIZE):
        batch = members[i : i + MAX_BATCH_SIZE]

        payload = {
            "members@odata.bind": [
                PAYLOAD_URL.format(quote_plus(member_id)) for member_id in batch
            ]
        }

        response = client.patch(url, headers=headers, json=payload, timeout=timeout)
        total_seconds += response.elapsed.total_seconds()

        if response.status_code != 204:
            error_message = "Request failed ({} {}) - {}".format(
                response.status_code,
                response.reason_phrase,
                response.json().get("error", {}).get("message"),
            )
            logger.error(error_message)
            raise ConnectionError(error_message)

        seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
        logger.debug(f"Added members {batch} in request {seconds_str}")

    total_seconds_str = "{:.1f} s".format(total_seconds)
    logger.info(f"Request completed successfully {total_seconds_str}")

    return True


def remove_group_member(
    group_id: str, member_id: str, timeout: float = DEFAULT_TIMEOUT
) -> bool:
    """
    Removes a member from a security group or M365 group.

    Requires admin consent for "GroupMember.ReadWrite.All" app permissions in the
    client.

    To remove members from a role-assignable group, the app must also be assigned
    the "RoleManagement.ReadWrite.Directory" permission.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/group-delete-members

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/groups/{}/members/{}/$ref"

    url = BASE_URL.format(quote_plus(group_id), quote_plus(member_id))
    headers = {"Authorization": f"Bearer {get_token()}"}

    logger.info(f"Removing member {member_id} from group {group_id} ..")

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
