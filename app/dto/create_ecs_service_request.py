from typing import Optional

from pydantic import BaseModel

from app.services.aws.models import AwsEcsFargateModel
from app.services.aws.security_group.ingress_rule_model import IngressRuleModel


class CreateECSServiceRequest(BaseModel):
    stack_name: Optional[str] = None
    project_name: Optional[str] = None
    ecs_fargate: AwsEcsFargateModel
    ingress_rule: Optional[IngressRuleModel] = None
    egress_rule: Optional[IngressRuleModel] = None

