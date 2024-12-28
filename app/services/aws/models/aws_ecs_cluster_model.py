from typing import Optional

from pydantic import BaseModel


class AwsEcsClusterModel(BaseModel):
    cluster_name: str
    enabled: Optional[bool] = True
