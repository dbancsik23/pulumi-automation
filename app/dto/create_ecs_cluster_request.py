from typing import Optional

from pydantic import BaseModel

from app.services.aws.models import AwsEcsClusterModel


class CreateECSClusterRequest(BaseModel):
    stack_name: Optional[str] = None
    project_name: Optional[str] = None
    ecs_cluster: AwsEcsClusterModel
