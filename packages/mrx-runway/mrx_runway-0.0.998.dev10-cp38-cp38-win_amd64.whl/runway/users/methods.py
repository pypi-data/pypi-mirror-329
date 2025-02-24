#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2025] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
#
import urllib.parse
from typing import Any, Dict
from urllib.parse import SplitResult

from runway.common.utils import save_settings_to_dotenv
from runway.settings import settings
from runway.users.api_client import (
    fetch_user_profile,
    login_and_get_token,
    logout_and_delete_token,
)
from runway.users.schemas import TokenInfo, UserInfo


def login(runway_url: str, email: str, password: str) -> TokenInfo:
    """
    Login to Runway and Get a SDK token.

    Parameters
    ----------
    runway_url : str
        The URL of Runway
    email : str
        Email
    password : str
        Password

    Returns
    -------
    TokenInfo
        A structure containing SDK token information

    Examples
    --------
    >>> import runway
    >>> runway.login(runway_url="http://runway.example.com", email="user@example.com", password="...")
    TokenInfo(id=1, token=..., masked_token=..., created_at=1732863878, used_at=None)
    """
    parsed_url: SplitResult = urllib.parse.urlsplit(url=runway_url)
    if parsed_url.scheme:
        settings.RUNWAY_API_PROTOCOL = parsed_url.scheme
        settings.RUNWAY_API_SERVER_URL = parsed_url.netloc
    else:
        settings.RUNWAY_API_SERVER_URL = parsed_url.path

    token_info: Dict[str, Any] = login_and_get_token(email=email, password=password)

    settings.RUNWAY_USER_ID = str(token_info["user_id"])
    settings.RUNWAY_SDK_TOKEN = token_info["token"]

    save_settings_to_dotenv()

    return TokenInfo(**token_info)


def logout() -> None:
    """
    Logout from Runway and Delete the SDK token.

    Raises
    ------
    ValueError
        If the user is not logged in and the RUNWAY_SDK_TOKEN is not set

    Examples
    --------
    >>> import runway
    >>> runway.logout()
    """
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError("RUNWAY_SDK_TOKEN is not set. Please call login() first.")

    logout_and_delete_token(token=settings.RUNWAY_SDK_TOKEN)

    settings.RUNWAY_SDK_TOKEN = ""
    settings.RUNWAY_WORKSPACE_ID = ""
    settings.RUNWAY_PROJECT_ID = ""

    settings.unset_launch_params()
    settings.unset_model_registry()

    save_settings_to_dotenv()


def get_user_profile() -> UserInfo:
    """
    Get the profile of the user.

    Returns
    -------
    UserInfo
        A structure containing user information

    Raises
    ------
    ValueError
        If the user is not logged in and the RUNWAY_SDK_TOKEN is not set

    Examples
    --------
    >>> import runway
    >>> runway.get_user_profile()
    UserInfo(id=1, email=user@example.com, first_name=Makina, last_name=Rocks, created_at=1732863878, extra=None, \
country_code=..., phone_number=...)
    """
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError("RUNWAY_SDK_TOKEN is not set. Please call login() first.")

    user_info: Dict[str, Any] = fetch_user_profile()

    return UserInfo(**user_info)
