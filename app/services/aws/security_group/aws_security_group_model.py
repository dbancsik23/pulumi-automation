from typing import List, Optional, Dict

from pydantic import BaseModel

from app.services.aws.security_group.ingress_rule_model import IngressRuleModel


class AwsSecurityGroupModel(BaseModel):
    name: str
    enabled: Optional[bool] = True
    vpc_id: str
    ingress: List[IngressRuleModel]
    egress: Optional[List[Dict]] = None