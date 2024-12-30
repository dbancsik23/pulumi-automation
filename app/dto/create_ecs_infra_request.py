from typing import Optional

from pydantic import BaseModel

from app.dto.create_ecs_cluster_request import CreateECSClusterRequest
from app.dto.create_ecs_service_request import CreateECSServiceRequest


class CreateECSInfraRequest(BaseModel):
    stack_name: str
    project_name: str
    ecs_cluster: list[CreateECSClusterRequest]
    ecs_fargate_services: Optional[list[CreateECSServiceRequest]] = None
