from pydantic import BaseModel

from app.services.aws.models import AwsEcsClusterModel


class CreateECSClusterRequest(BaseModel):
    stack_name: str
    project_name: str
    ecs_fargate: AwsEcsClusterModel

    def to_dict(self):
        return self.model_dump()
