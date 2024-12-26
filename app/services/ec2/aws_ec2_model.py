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
    _user_data_base64: Optional[str] = None
