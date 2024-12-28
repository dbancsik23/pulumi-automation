from fastapi import APIRouter
from pulumi import automation as auto

from app.dto.list_stacks_request import ListStackRequest
from app.security.command_validator import permit_only
from app.services.pulumi.pulumi_commands import PulumiCommands

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
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.DESTROY])
def list_stacks(body: ListStackRequest):
    ws = auto.LocalWorkspace(project_settings=auto.ProjectSettings(name=body.project_name, runtime="python"))
    return ws.list_stacks()
