from typing import List, Dict, Optional

from pydantic import BaseModel

from app.services.aws.ecs.container_definition_model import ContainerDefinitionModel


class AwsEcsFargateModel(BaseModel):
    name: str
    cpu: Optional[str] = "256"
    memory: Optional[str] = "512"
    subnet_ids: List[str]
    vpc_id: str
    port: Optional[int] = 8080
    container_definitions: ContainerDefinitionModel
    vpc_security_group_ids: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None
    task_role_arn: Optional[str] = None
    execution_role_arn: Optional[str] = None
    desired_count: Optional[int] = 1
    enable_load_balancer: Optional[bool] = False
    load_balancer_config: Optional[Dict] = None
    enabled: Optional[bool] = True
    cluster_name: Optional[str] = None
    assign_public_ip: Optional[bool] = False
    inline_policies: Optional[Dict[str, str]] = None
