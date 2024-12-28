from fastapi import APIRouter

from app.dto.delete_stack_request import DeleteStackRequest
from app.security.command_validator import permit_only
from app.services.pulumi.pulumi_commands import PulumiCommands
from app.services.pulumi.pulumi_stack_service import PulumiStackService

router = APIRouter(
    prefix="/destroy",
    tags=["Stack and Resource Destroy"]
)


@router.delete("/stack",
               summary="Delete stack",
               description="Delete stack with provided stack name.",
               response_description="Stack deleted successfully.")
@permit_only([PulumiCommands.DESTROY, PulumiCommands.PREVIEW])
def delete_stack(body: DeleteStackRequest, action: PulumiCommands):
    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=lambda *args: None)
    return stack.execute_stack_operation(action)