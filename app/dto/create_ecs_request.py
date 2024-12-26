from pydantic import BaseModel

from app.services.ecs import AwsEcsFargateModel


class CreateECSRequest(BaseModel):
    stack_name: str
    project_name: str
    ecs_fargate: AwsEcsFargateModel

    def to_dict(self):
        return self.model_dump()
