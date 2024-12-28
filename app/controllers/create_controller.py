from fastapi import APIRouter

from app.dto.create_ec2_request import CreateEC2Request
from app.dto.create_ecs_cluster_request import CreateECSClusterRequest
from app.dto.create_ecs_service_request import CreateECSServiceRequest
from app.security.command_validator import permit_only
from app.services.pulumi.dto import PulumiCommands
from app.services.pulumi.pulumi_stack_service import PulumiStackService
from app.services.resource_manager import EC2ResourceManagerService
from app.services.resource_manager.ecs_cluster_resource_manager_service import ECSClusterResourceManagerService
from app.services.resource_manager.ecs_service_resource_manager_service import ECSServiceResourceManagerService

router = APIRouter(
    prefix="/create",
    tags=["Resource and Stack Creation"]
)

ECS_PREFIX = "/ecs"


@router.post("/ec2",
             summary="Create EC2 instance",
             description="Create EC2 instance with provided configuration.",
             response_description="EC2 instance created successfully.")
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ec2_service(body: CreateEC2Request, action: PulumiCommands):
    def pulumi_program():
        ec2_resource_manager = EC2ResourceManagerService(body)
        return ec2_resource_manager.create_resources()

    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=pulumi_program)
    return stack.execute_stack_operation(action)


@router.post(ECS_PREFIX + "/cluster",
             summary="Create ECS cluster",
             description="Create ECS cluster with provided Fargate configuration.",
             response_description="ECS cluster created successfully.")
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ecs_cluster(body: CreateECSClusterRequest, action: PulumiCommands):
    def pulumi_program():
        ecs_resource_manager = ECSClusterResourceManagerService(body.ecs_fargate)
        return ecs_resource_manager.create_resources()

    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=pulumi_program)
    return stack.execute_stack_operation(action)


@router.post(ECS_PREFIX + "/service",
             summary="Create ECS service",
             description="Create ECS service with provided task definition.",
             response_description="ECS service created successfully.")
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ecs_service(body: CreateECSServiceRequest, action: PulumiCommands):
    def pulumi_program():
        ecs_resource_manager = ECSServiceResourceManagerService(body)
        return ecs_resource_manager.create_resources()

    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=pulumi_program)
    return stack.execute_stack_operation(action)


@router.post(ECS_PREFIX + "/infra",
             summary="Create ECS infrastructure",
             description="Create complete ECS infrastructure including cluster, service, and task definition.",
             response_description="A list of stacks belonging to the specified project.")
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ecs_infra(body: CreateECSClusterRequest, action: PulumiCommands):
    def pulumi_program():
        ecs_resource_manager = EC2ResourceManagerService(body)
        return ecs_resource_manager.create_resources()

    stack = PulumiStackService(stack_name=body.stack_name, project_name=body.project_name,
                               program_name=pulumi_program)
    return stack.execute_stack_operation(action)
