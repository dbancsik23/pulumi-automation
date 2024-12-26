from typing import Optional

from pydantic import BaseModel

from app.services.ec2 import AwsEC2Model
from app.services.iam import AwsIAMRoleModel
from app.services.security_group.aws_security_group_model import AwsSecurityGroupModel


class CreateEC2Request(BaseModel):
    stack_name: str
    project_name: str
    security_group: Optional[AwsSecurityGroupModel]
    iam_role: Optional[AwsIAMRoleModel]
    ec2_instance: Optional[AwsEC2Model]

    def to_dict(self):
        return self.model_dump()
