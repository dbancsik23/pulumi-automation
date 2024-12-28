from typing import List, Optional, Dict

from pydantic import BaseModel


class AwsEC2Model(BaseModel):
    name: str
    instance_type: str
    ami_id: str
    subnet_id: str
    enabled: Optional[bool] = True
    key_name: Optional[str] = None
    additional_volumes: Optional[List[Dict[str, str]]] = None
    user_data: Optional[str] = None
    vpc_security_group_ids: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None
    launch_template: Optional[str] = None
    user_data_base64: Optional[str] = None
    private_ip: Optional[str] = None
    availability_zone: Optional[str] = None
    iam_instance_profile: Optional[str] = None
    associate_public_ip_address: Optional[bool] = False
