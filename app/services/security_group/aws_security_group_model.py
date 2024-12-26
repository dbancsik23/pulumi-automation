from dataclasses import field
from typing import List, Optional, Dict

import pulumi
from pydantic import BaseModel

from app.services.security_group.ingress_rule_model import IngressRuleModel


class AwsSecurityGroupModel(BaseModel):
    name: str
    enabled: Optional[bool] = True
    vpc_id: str
    ingress: List[IngressRuleModel]
    egress: Optional[List[Dict]] = None