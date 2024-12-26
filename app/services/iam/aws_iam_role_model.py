from typing import Optional, Dict, List

import pulumi_aws as aws
from pydantic import BaseModel


class AwsIAMRoleModel(BaseModel):
    name: str
    enabled: Optional[bool] = True
    assume_role_policy: Optional[str] = None
    description: Optional[str] = None
    max_session_duration: Optional[int] = None
    tags: Optional[Dict[str, str]] = None
    managed_policy_arns: Optional[List[str]] = None
    inline_policies: Optional[Dict[str, str]] = None
    enable_instance_profile: bool = True