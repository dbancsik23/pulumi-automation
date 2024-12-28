from typing import Dict

from app.dto.create_ecs_cluster_request import CreateECSClusterRequest
from app.services.aws.ecs.aws_ecs_cluster import AwsEcsCluster
from app.services.resource_manager import ResourceManager


class ECSClusterResourceManagerService(ResourceManager):
    def __init__(self, config: CreateECSClusterRequest):
        self.config = config
        self.result = {}

    def create_resources(self) -> Dict:
        return AwsEcsCluster(self.config).create_cluster()
