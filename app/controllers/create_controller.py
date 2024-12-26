from fastapi import APIRouter

from app.dto import CreateEC2Request
from app.dto.create_ecs_request import CreateECSRequest
from app.security.command_validator import permit_only
from app.services.pulumi.dto import PulumiCommands
from app.services.pulumi.pulumi_stack_service import PulumiStackService
from app.services.resource_manager import EC2ResourceManagerService

router = APIRouter(
    prefix="/create",
    tags=["Resource and Stack Creation"]
)
CREATE_PREFIX = "/create"


@router.post("/ec2")
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ec2_service(body: CreateEC2Request, action: PulumiCommands):
    def pulumi_program():
        ec2_resource_manager = EC2ResourceManagerService(body)
        return ec2_resource_manager.create_resources()

    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=pulumi_program)
    return stack.execute_stack_operation(action)


@router.post("/ecs")
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ecs_service(body: CreateECSRequest, action: PulumiCommands):
    def pulumi_program():
        ecs_resource_manager = EC2ResourceManagerService(body)
        return ecs_resource_manager.create_resources()

    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=pulumi_program)
    return stack.execute_stack_operation(action)
