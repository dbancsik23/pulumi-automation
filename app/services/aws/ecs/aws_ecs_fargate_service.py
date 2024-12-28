import json
from typing import Dict

import pulumi
import pulumi_aws as aws
from pulumi_aws.ecs import ServiceLoadBalancerArgs

from app.services.aws.ecs.container_definition_model import ContainerDefinitionModel
from app.services.aws.models import AwsEcsFargateModel
from app.services.helper.pulumi_helper import PulumiHelper as helper


class AwsECSFargate:

    def __init__(
            self,
            model: AwsEcsFargateModel
    ):
        self.enabled = model.enabled
        self.env = pulumi.get_stack()
        self.name = f"{model.name}-{self.env}"
        self.container_definitions = model.container_definitions
        self.cpu = model.cpu
        self.memory = model.memory
        self.port = model.port
        self.vpc_security_group_ids = model.vpc_security_group_ids or []
        self.subnet_ids = model.subnet_ids or []
        self.default_tags = helper.default_tags(self.name)
        self.tags = model.tags or self.default_tags
        self.task_role_arn = model.task_role_arn
        self.execution_role_arn = model.execution_role_arn
        self.desired_count = model.desired_count
        self.enable_load_balancer = model.enable_load_balancer
        self.load_balancer_config = model.load_balancer_config or {}
        self.assign_public_ip = model.assign_public_ip
        self.cluster_name = self.get_cluster_name(model.cluster_name)

    def create_fargate_service(self):

        task_definition = aws.ecs.TaskDefinition(
            self.name,
            family=self.name,
            cpu=self.cpu,
            memory=self.memory,
            network_mode="awsvpc",
            requires_compatibilities=["FARGATE"],
            execution_role_arn=self.execution_role_arn,
            task_role_arn=self.task_role_arn,
            container_definitions=json.dumps([self.generate_container_definition(self.container_definitions)]),
            tags=self.tags
        )

        network_configuration = {
            "subnets": self.subnet_ids,
            "security_groups": self.vpc_security_group_ids,
            "assign_public_ip": self.assign_public_ip
        }

        service_args = {
            "cluster": self.cluster_name,
            "desired_count": self.desired_count,
            "launch_type": "FARGATE",
            "task_definition": task_definition.arn,
            "network_configuration": network_configuration,
            "tags": self.tags
        }

        if self.enable_load_balancer and self.load_balancer_config:
            load_balancers = [ServiceLoadBalancerArgs(
                target_group_arn=self.load_balancer_config.get("target_group_arn"),
                container_name=self.load_balancer_config.get("container_name"),
                container_port=self.load_balancer_config.get("container_port")
            )]
            service_args["load_balancers"] = load_balancers

        service = aws.ecs.Service(
            self.name,
            **service_args
        )

        pulumi.export(f"{self.name}_task_definition_arn", task_definition.arn)
        pulumi.export(f"{self.name}_service_name", service.name)
        pulumi.export(
            f"{self.name}_details",
            service.id.apply(lambda id: f"Fargate Service {self.name} created with ID: {id}")
        )

    def generate_container_definition(self, config: ContainerDefinitionModel) -> Dict:
        container_def = {
            "name": config.container_name,
            "image": config.image,
            "essential": True,
            "portMappings": [{
                "containerPort": self.port,
                "hostPort": self.port,
            }],
        }

        if config.environment:
            container_def["environment"] = config.environment
        if config.secrets:
            container_def["secrets"] = config.secrets
        if config.log_configuration:
            container_def["logConfiguration"] = config.log_configuration

        return container_def

    @staticmethod
    def get_cluster_name(cluster_name: str):
        return aws.ecs.get_cluster(cluster_name=cluster_name).id
