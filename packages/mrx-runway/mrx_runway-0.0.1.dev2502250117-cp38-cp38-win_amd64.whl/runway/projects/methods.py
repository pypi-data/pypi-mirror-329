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
from runway.model_registry.methods.methods import (
    get_model_registry_list,
    set_model_registry,
)
from runway.model_registry.schemas import ModelRegistryInfo
from runway.projects.api_client import fetch_joined_projects, fetch_user_project_role
from runway.projects.schemas import ProjectInfo
from runway.settings import RunwayLaunchParameters, RunwayLinkSource, settings


def get_joined_projects() -> List[ProjectInfo]:
    """
    Get a list of projects that the user has joined within the currently selected workspace.

    Returns
    -------
    List[ProjectInfo]
        A list of structures containing project information

    Raises
    ------
    ValueError
        - If the user is not logged in and the RUNWAY_SDK_TOKEN is not set
        - If no workspace is currently selected and the RUNWAY_WORKSPACE_ID is not set

    Examples
    --------
    >>> import runway
    >>> runway.get_joined_projects()
    [ProjectInfo(id=1, title=MyProject, description=None, created_at=1732863878, updated_at=1732863878, owner={...}, \
directory_name=project-1-00001, kubernetes_namespace=runway-project-0001, backup_status=active, favorite=False, \
status=joined, join_status=joined), ...]
    """
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )
    if not settings.RUNWAY_WORKSPACE_ID:
        raise ValueError(
            "RUNWAY_WORKSPACE_ID is not set. Please call set_joined_workspace() first.",
        )
    projects = fetch_joined_projects()
    for project in projects:
        project_id = project["id"]
        user_project_role = fetch_user_project_role(project_id)
        project["project_role"] = user_project_role["project_role"]
    return [ProjectInfo(**project) for project in projects]


def set_joined_project(project_id: int) -> None:
    """
    Select and set a project from the joined projects using the ID.

    Parameters
    ----------
    project_id : int
        The ID of the project to select from the joined projects

    Raises
    ------
    ValueError
        - If the user is not logged in and the RUNWAY_SDK_TOKEN is not set
        - If no workspace is currently selected and the RUNWAY_WORKSPACE_ID is not set

    Examples
    --------
    >>> import runway
    >>> runway.set_joined_workspaces(project_id=1)
    """
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )
    if not settings.RUNWAY_WORKSPACE_ID:
        raise ValueError(
            "RUNWAY_WORKSPACE_ID is not set. Please call set_joined_workspace() first.",
        )

    projects: List[Dict[str, Any]] = fetch_joined_projects()

    project: Dict[str, Any] = next((p for p in projects if p["id"] == project_id), {})
    if not project:
        raise ValueError(
            f"Project ID {project_id} not found in the joined projects. Please provide a valid project ID.",
        )

    settings.RUNWAY_PROJECT_ID = str(project_id)
    settings.RUNWAY_PROJECT_DIR = project["directory_name"]

    launch_params: RunwayLaunchParameters = RunwayLaunchParameters(
        source=RunwayLinkSource(
            entityname="dev_instance",
            resource_id=1,
            dev_instance_type="custom",
        ),
    )
    settings.set_launch_params(launch_params)

    model_registry_list: List[ModelRegistryInfo] = get_model_registry_list()
    model_registries: List[Dict[str, Any]] = [
        model_registry.to_dict() for model_registry in model_registry_list
    ]
    mlflow_registry: Dict[str, Any] = next(
        (
            mr
            for mr in model_registries
            if mr["name"] == "Runway-mlflow" and mr["type"] == "mlflow"
        ),
        {},
    )
    if not mlflow_registry:
        raise ValueError("Runway-mlflow model registry not found")
    set_model_registry(model_registry_id=mlflow_registry["id"])

    save_settings_to_dotenv()
