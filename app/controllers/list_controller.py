from fastapi import APIRouter
from pulumi import automation as auto

from app.dto.delete_stack_request import DeleteStackRequest

router = APIRouter(
    prefix="/list",
    tags=["Stack detail listing"]
)


@router.post("/stacks")
def list_stacks(body: DeleteStackRequest):
    ws = auto.LocalWorkspace(project_settings=auto.ProjectSettings(name=body.project_name, runtime="python"))
    return ws.list_stacks()
