import pulumi
import pulumi_aws as aws

from app.services.aws.models.aws_ecs_cluster_model import AwsEcsClusterModel
from app.services.helper.pulumi_helper import PulumiHelper as helper


class AwsEcsCluster:
    def __init__(self, model: AwsEcsClusterModel):
        self.cluster_name = model.cluster_name
        self.env = pulumi.get_stack()
        self.tags = helper.default_tags(self.cluster_name)
        self.enabled = model.enabled

    def create_cluster(self):
        cluster = aws.ecs.Cluster(
            f"{self.cluster_name}-{self.env}",
            name=f"{self.cluster_name}-{self.env}",
            tags=self.tags
        )
        pulumi.log.info(f"Cluster {self.cluster_name} created successfully.")
        pulumi.export(f"{self.cluster_name}_cluster_name", cluster.name)
        return cluster.arn
