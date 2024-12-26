from typing import Optional

from pydantic import BaseModel

from libs.ec2 import AwsEC2Model
from libs.iam import AwsIAMRoleModel
from libs.security_group.aws_security_group_model import AwsSecurityGroupModel


class ListStackRequest(BaseModel):
    project_name: str
