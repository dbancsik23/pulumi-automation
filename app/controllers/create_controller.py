import logging

from fastapi import APIRouter

from app.dto.create_ec2_request import CreateEC2Request
from app.dto.create_ecs_cluster_request import CreateECSClusterRequest
from app.dto.create_ecs_infra_request import CreateECSInfraRequest
from app.dto.create_ecs_service_request import CreateECSServiceRequest
from app.security.command_validator import permit_only
from app.services.pulumi.pulumi_commands import PulumiCommands
from app.services.pulumi.pulumi_stack_service import PulumiStackService
from app.services.resource_manager import EC2ResourceManagerService
from app.services.resource_manager.ecs_cluster_resource_manager_service import ECSClusterResourceManagerService
from app.services.resource_manager.ecs_service_resource_manager_service import ECSServiceResourceManagerService

router = APIRouter(
    prefix="/manage-resources",
    tags=["Resource and Stack Management including create and update"]
)

ECS_PREFIX = "/ecs"


@router.post("/ec2",
             summary="Create/Update EC2 instance",
             description="Create/Update EC2 instance with provided configuration.",
             status_code=201)
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ec2_service(body: CreateEC2Request, action: PulumiCommands):
    return handle_stack_operation(
        body.stack_name,
        body.project_name,
        action,
        lambda: EC2ResourceManagerService(body).create_resources(),
        body=body.model_dump_json()
    )


@router.post(ECS_PREFIX + "/cluster",
             summary="Create/Update ECS cluster",
             description="Create/Update ECS cluster with provided Fargate configuration.",
             status_code=201)
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ecs_cluster(body: CreateECSClusterRequest, action: PulumiCommands):
    return handle_stack_operation(
        body.stack_name,
        body.project_name,
        action,
        lambda: ECSClusterResourceManagerService(body.ecs_cluster).create_resources(),
        body=body.model_dump_json()
    )


@router.post(ECS_PREFIX + "/service",
             summary="Create/Update ECS service",
             description="Create/Update ECS service with provided task definition.",
             status_code=201)
@permit_only([PulumiCommands.PREVIEW, PulumiCommands.UP])
def ecs_service(body: CreateECSServiceRequest, action: PulumiCommands):
    return handle_stack_operation(
        body.stack_name,
        body.project_name,
        action,
        lambda: ECSServiceResourceManagerService(body, action).create_resources(),
        body=body.model_dump_json()
    )


@router.post(ECS_PREFIX + "/infra",
             summary="Create/Update ECS infrastructure",
             description="Create/Update complete ECS infrastructure including cluster, service, and task definition.",
             response_description="A list of stacks belonging to the specified project.",
             status_code=201)
@permit_only([PulumiCommands.UP])
def ecs_infra(body: CreateECSInfraRequest, action: PulumiCommands):
    response = {}
    try:
        response["clusters"] = [create_cluster(cluster, action, body.project_name) for cluster in
                                body.ecs_cluster]
        response["services"] = [create_service(service, action, body.project_name) for service in
                                (body.ecs_fargate_services or [])]
        return response
    except Exception as e:
        logging.error(f"Error during resource creation, message: {str(e)}")


def handle_stack_operation(stack_name: str, project_name: str, action: PulumiCommands, program, body: str):
    stack_service = PulumiStackService(
        stack_name=stack_name,
        project_name=project_name,
        program_name=program

    )
    return stack_service.execute_stack_operation(action, project_name, body)


def create_cluster(body: CreateECSClusterRequest, action: PulumiCommands, project_name: str):
    stack_name = f"{project_name}-{body.ecs_cluster.cluster_name}"
    return handle_stack_operation(
        stack_name,
        project_name,
        action,
        lambda: ECSClusterResourceManagerService(body.ecs_cluster).create_resources(),
        body=body.model_dump_json())


def create_service(body: CreateECSServiceRequest, action: PulumiCommands, project_name: str):
    stack_name = f"{project_name}-{body.ecs_fargate.name}"
    handle_stack_operation(
        stack_name,
        project_name,
        action,
        lambda: ECSServiceResourceManagerService(body.ecs_fargate).create_resources(),
        body=body.model_dump_json())
