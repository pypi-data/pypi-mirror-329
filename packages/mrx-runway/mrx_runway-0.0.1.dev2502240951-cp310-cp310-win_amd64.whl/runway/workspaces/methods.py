# MAKINAROCKS CONFIDENTIAL
# ________________________
#
# [2017] - [2025] MakinaRocks Co., Ltd.
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of MakinaRocks Co., Ltd. and its suppliers, if any.
# The intellectual and technical concepts contained herein are
# proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
# covered by U.S. and Foreign Patents, patents in process, and
# are protected by trade secret or copyright law. Dissemination
# of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained
# from MakinaRocks Co., Ltd.
from typing import Any, Dict, List

from runway.common.utils import save_settings_to_dotenv
from runway.settings import settings
from runway.workspaces.api_client import (
    fetch_joined_workspaces,
    fetch_user_role_in_workspace,
)
from runway.workspaces.schemas import WorkspaceInfo


def get_joined_workspaces() -> List[WorkspaceInfo]:
    """
    Get a list of joined workspaces.

    Returns
    -------
    List[WorkspaceInfo]
        A list of structures containing workspace information

    Raises
    ------
    ValueError
        If the user is not logged in and the RUNWAY_SDK_TOKEN is not set

    Examples
    --------
    >>> import runway
    >>> runway.get_joined_workspaces()
    [WorkspaceInfo(id=1, name=MyWorkspace, description=None, resource={...}, is_limited=False, created_at=1732863878, \
activated_at=1732863878, expired_at=None, status=active, user_count=4, members_seat=10, members_concurrent=5, viewers_seat=20, \
nodes=[...], ), ...]
    """
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )

    workspaces: List[Dict[str, Any]] = fetch_joined_workspaces()
    for workspace in workspaces:
        workspace_id: int = workspace["id"]
        user_role: Dict[str, Any] = fetch_user_role_in_workspace(
            workspace_id=workspace_id,
        )
        workspace["workspace_role"] = str(user_role["workspace_role"])

    return [WorkspaceInfo(**workspace) for workspace in workspaces]


def set_joined_workspace(workspace_id: int) -> None:
    """
    Select and set a workspace from the joined workspaces using the ID.

    Parameters
    ----------
    workspace_id : int
        The ID of the workspace to select from the joined workspaces

    Raises
    ------
    ValueError
        If the user is not logged in and the RUNWAY_SDK_TOKEN is not set

    Examples
    --------
    >>> import runway
    >>> runway.set_joined_workspaces(workspace_id=1)
    """
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )

    settings.RUNWAY_WORKSPACE_ID = str(workspace_id)

    save_settings_to_dotenv()
