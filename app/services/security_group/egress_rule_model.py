from pydantic import BaseModel

from app.services.security_group.rule_type import RuleType


class IngressRuleModel(BaseModel):
    rule_type: str = RuleType.EGRESS.name.lower()
    protocol: str = "tcp"
    from_port: int
    to_port: int
    cidr_blocks: list[str]
