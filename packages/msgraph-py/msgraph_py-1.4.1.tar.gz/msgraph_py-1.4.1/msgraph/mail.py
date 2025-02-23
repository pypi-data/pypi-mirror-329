import base64
import json
import logging
import mimetypes
import os.path
from typing import Union
from urllib.parse import quote_plus

from .core import DEFAULT_TIMEOUT, ensure_list, get_http_client, get_token

VALID_PRIORITY = ["low", "normal", "high"]

logger = logging.getLogger(__name__)


def send_mail(
    sender_id: str,
    recipients: Union[list[str], str],
    subject: str,
    body: str,
    is_html: bool = False,
    priority: str = "normal",
    recipients_cc: Union[list[str], str] = [],
    recipients_bcc: Union[list[str], str] = [],
    attachments: Union[list[str], str] = [],
    save_sent_items: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> bool:
    """
    Sends an email on behalf of a user via the Microsoft Graph API.
    Does not save sent items unless save_sent_items=True is set.

    Attachments are added as file paths in the attachments parameter.
    The total size with attachments must not exceed 3MB:
    https://learn.microsoft.com/en-us/graph/api/resources/fileattachment

    Requires admin consent for "Mail.Send" app permissions in the AAD client.

    Note that this permission grants the app access to send emails as any
    user in the organization. This can be restricted with an application access policy:
    https://learn.microsoft.com/en-us/graph/auth-limit-mailbox-access

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/user-sendmail

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/users/{}/sendMail"

    if priority.lower() not in VALID_PRIORITY:
        raise ValueError(
            f"Parameter priority='{priority}' is not a valid value {VALID_PRIORITY}"
        )

    content_type = "HTML" if is_html else "Text"

    recipients = ensure_list(recipients)
    recipients_cc = ensure_list(recipients_cc)
    recipients_bcc = ensure_list(recipients_bcc)
    attachments = ensure_list(attachments)

    attachments_formatted = []

    for path in attachments:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File '{path}' was not found.")

        with open(path, mode="rb") as binary:
            encoded_attachment = base64.b64encode(binary.read()).decode("utf-8")

        attachments_formatted.append(
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": os.path.basename(path),
                "contentType": mimetypes.guess_type(path)[0],
                "contentBytes": encoded_attachment,
            }
        )

    url = BASE_URL.format(quote_plus(sender_id))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_token()}",
    }
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": content_type, "content": body},
            "toRecipients": [
                {"emailAddress": {"address": address}} for address in recipients
            ],
            "ccRecipients": [
                {"emailAddress": {"address": address}} for address in recipients_cc
            ],
            "bccRecipients": [
                {"emailAddress": {"address": address}} for address in recipients_bcc
            ],
            "importance": priority,
            "attachments": attachments_formatted,
        },
        "saveToSentItems": save_sent_items,
    }

    logger.debug(f"Payload content:\n{json.dumps(payload, indent=2)}")
    logger.info(f"Sending mail from {sender_id} to {recipients}")

    client = get_http_client()
    response = client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 202:
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
