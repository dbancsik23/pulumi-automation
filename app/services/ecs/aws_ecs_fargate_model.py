from typing import List, Dict, Optional

from pydantic import BaseModel

from app.services.ecs import ContainerDefinitionModel


class AwsEcsFargateModel(BaseModel):
    name: str
    cluster_name: str
    cpu: str
    memory: str
    container_definitions: ContainerDefinitionModel
    vpc_security_group_ids: Optional[List[str]]
    subnet_ids: Optional[List[str]]
    tags: Optional[Dict[str, str]]
    task_role_arn: Optional[str]
    execution_role_arn: Optional[str]
    desired_count: Optional[int]
    enable_load_balancer: Optional[bool]
    load_balancer_config: Optional[Dict]
    enabled: Optional[bool] = True
