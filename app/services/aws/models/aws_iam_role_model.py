from typing import Optional, Dict, List

from pydantic import BaseModel


class AwsIAMRoleModel(BaseModel):
    name: str
    enabled: Optional[bool] = True
    assume_role_policy: Optional[str] = None
    description: Optional[str] = None
    max_session_duration: Optional[int] = 3600
    tags: Optional[Dict[str, str]] = None
    managed_policy_arns: Optional[List[str]] = None
    inline_policies: Optional[Dict[str, str]] = None
    enable_instance_profile: bool = True