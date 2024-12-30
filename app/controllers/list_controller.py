import json

from fastapi import APIRouter
from pulumi import automation as auto

from app.dto.list_stacks_request import ListStackRequest
from app.repository.stack_config_repo import *

router = APIRouter(
    prefix="/list",
    tags=["Stack detail listing"]
)


@router.post(
    "/stacks",
    summary="List all stacks",
    description="Lists all stacks for the provided project name.",
    response_description="A list of stacks belonging to the specified project."
)
def list_stacks(body: ListStackRequest):
    ws = auto.LocalWorkspace(project_settings=auto.ProjectSettings(name=body.project_name, runtime="python"))
    return ws.list_stacks()


@router.get("/stacks/{project_name}/{stack_name}",
            summary="Get stack details",
            description="Get config details for the provided project name.")
def get_project(project_name: str, stack_name: str):
    return json.loads(get_by_project_and_stack(project_name, stack_name).stack_configuration)
