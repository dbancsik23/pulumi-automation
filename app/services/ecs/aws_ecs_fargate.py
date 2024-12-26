from dataclasses import dataclass
from typing import Optional, List, Dict

import pulumi
import pulumi_aws as aws
from pulumi_aws.ecs import ServiceLoadBalancerArgs

from app.services.helper.pulumi_helper import PulumiHelper as helper
from app.services.ecs import ContainerDefinitionModel


@dataclass(init=False)
class AwsECSFargate:
    name: str
    cluster_name: str
    container_definitions: ContainerDefinitionModel
    cpu: str
    memory: str
    vpc_security_group_ids: Optional[List[str]]
    subnet_ids: Optional[List[str]]
    tags: Optional[Dict[str, str]]
    task_role_arn: Optional[str]
    execution_role_arn: Optional[str]
    desired_count: Optional[int]
    enable_load_balancer: Optional[bool]
    load_balancer_config: Optional[Dict]
    enabled: Optional[bool] = True

    def __init__(
            self,
            name: str,
            cluster_name: str,
            container_definitions: ContainerDefinitionModel,
            cpu: str,
            memory: str,
            enabled: Optional[bool] = True,
            vpc_security_group_ids: Optional[List[str]] = None,
            subnet_ids: Optional[List[str]] = None,
            tags: Optional[Dict[str, str]] = None,
            task_role_arn: Optional[str] = None,
            execution_role_arn: Optional[str] = None,
            desired_count: Optional[int] = 1,
            enable_load_balancer: Optional[bool] = False,
            load_balancer_config: Optional[Dict] = None,
            assign_public_ip: Optional[bool] = False
    ):
        self.enabled = enabled
        self.env = pulumi.get_stack()
        self.name = f"{name}-{self.env}"
        self.cluster_name = cluster_name
        self.container_definitions = container_definitions
        self.cpu = cpu
        self.memory = memory
        self.vpc_security_group_ids = vpc_security_group_ids or []
        self.subnet_ids = subnet_ids or []
        self.default_tags = helper.default_tags(self.name)
        self.tags = tags or self.default_tags
        self.task_role_arn = task_role_arn
        self.execution_role_arn = execution_role_arn
        self.desired_count = desired_count
        self.enable_load_balancer = enable_load_balancer
        self.load_balancer_config = load_balancer_config or {}
        self.assign_public_ip = assign_public_ip

    def create_fargate_service(self):
        cluster = aws.ecs.Cluster(
            f"{self.cluster_name}-{self.env}",
            name=f"{self.cluster_name}-{self.env}",
            tags=self.tags
        )

        task_definition = aws.ecs.TaskDefinition(
            self.name,
            family=self.name,
            cpu=self.cpu,
            memory=self.memory,
            network_mode="awsvpc",
            requires_compatibilities=["FARGATE"],
            execution_role_arn=self.execution_role_arn,
            task_role_arn=self.task_role_arn,
            container_definitions=str([self.generate_container_definition(**self.container_definitions)]),
            tags=self.tags
        )

        network_configuration = {
            "subnets": self.subnet_ids,
            "security_groups": self.vpc_security_group_ids,
            "assign_public_ip": self.assign_public_ip
        }

        service_args = {
            "cluster": cluster.arn,
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

        pulumi.export(f"{self.name}_cluster_name", cluster.name)
        pulumi.export(f"{self.name}_task_definition_arn", task_definition.arn)
        pulumi.export(f"{self.name}_service_name", service.name)
        pulumi.export(
            f"{self.name}_details",
            service.id.apply(lambda id: f"Fargate Service {self.name} created with ID: {id}")
        )

    @staticmethod
    def generate_container_definition(config: ContainerDefinitionModel) -> Dict:
        container_def = {
            "name": config.container_name,
            "image": config.image,
            "essential": True
        }

        if config.port_mappings:
            container_def["portMappings"] = config.port_mappings
        if config.environment:
            container_def["environment"] = config.environment
        if config.secrets:
            container_def["secrets"] = config.secrets
        if config.log_configuration:
            container_def["logConfiguration"] = config.log_configuration

        return container_def
