import logging

from .devices import (  # noqa: F401
    delete_device,
    get_bitlocker_key,
    get_device,
    get_device_bitlocker_key,
    get_laps_password,
    list_owned_devices,
)
from .groups import (  # noqa: F401
    add_group_member,
    get_group,
    list_group_members,
    remove_group_member,
)
from .identity import (  # noqa: F401
    delete_auth_method,
    get_signin,
    get_user,
    get_user_risk,
    list_auth_methods,
    reset_strong_auth,
    revoke_refresh_tokens,
)
from .mail import (  # noqa: F401
    send_mail,
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
