from app.dto.create_ecs_service_request import CreateECSServiceRequest
from app.services.aws.ecs.aws_ecs_fargate_service import AwsECSFargate
from app.services.aws.iam import AssumeRoleService
from app.services.aws.models import AwsIAMRoleModel, AwsEcsFargateModel
from app.services.aws.security_group.aws_security_group_model import AwsSecurityGroupModel
from app.services.aws.security_group.ingress_rule_model import IngressRuleModel
from app.services.factory.resource_factory import ResourceFactory as factory
from app.services.helper.pulumi_helper import PulumiHelper as helper
from app.services.resource_manager import ResourceManager


class ECSServiceResourceManagerService(ResourceManager):
    EXECUTION_ROLE_POLICY = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"

    def __init__(self, config: CreateECSServiceRequest):
        self.config = config
        self.resources = {}
        self.env = config.stack_name
        self.service_name = self.config.ecs_fargate.name

    def create_resources(self) -> dict:
        ecs_service = self.initialize_ecs_service()

        if not self.config.ecs_fargate.vpc_security_group_ids:
            ecs_service.vpc_security_group_ids = [self.create_security_group()["sg_id"]]

        if not self.config.ecs_fargate.task_role_arn:
            ecs_service.iam_role = self.create_fargate_iam_role()["role_arn"]

        execution_role = self.create_fargate_execution_role()
        ecs_service.execution_role_arn = execution_role["role_arn"]

        ecs_service.create_fargate_service()

        self.resources["service"] = ecs_service
        return self.resources

    def initialize_ecs_service(self) -> AwsECSFargate:
        return factory.build(AwsEcsFargateModel(**self.config.ecs_fargate.model_dump()))

    def create_security_group(self) -> dict | None:
        if not self.config.ecs_fargate.vpc_security_group_ids:
            security_group = self.create_default_security_group()
            self.resources["security_group"] = security_group
            return security_group
        if self.config.ingress_rule or self.config.egress_rule:
            return self.create_custom_security_group()
        return None

    def create_custom_security_group(self) -> dict:
        return factory.build(AwsSecurityGroupModel(
            name=self.config.ecs_fargate.name,
            vpc_id=self.config.ecs_fargate.vpc_id,
            ingress=self.config.ecs_fargate.ingress_rule,
            egress=self.config.ecs_fargate.egress_rule
        )).create_security_group()

    def create_default_security_group(self) -> dict:
        return factory.build(AwsSecurityGroupModel(
            name=f"{self.config.ecs_fargate.name}-default",
            vpc_id=self.config.ecs_fargate.vpc_id,
            ingress=[self.create_default_ingress_rule()]
        )).create_security_group()

    def create_fargate_execution_role(self) -> dict:
        return factory.build(AwsIAMRoleModel(
            enabled=True,
            name=f"{self.service_name}-ecs-execution",
            assume_role_policy=AssumeRoleService.ECS_TASK.value,
            description=f"IAM execution role for {self.service_name}-{self.env}",
            tags=helper.default_tags(self.service_name),
            managed_policy_arns=[self.EXECUTION_ROLE_POLICY],
            enable_instance_profile=False
        )).create_role()

    def create_fargate_iam_role(self) -> dict:
        return factory.build(AwsIAMRoleModel(
            name=f"{self.service_name}-ecs-task",
            assume_role_policy=AssumeRoleService.ECS_TASK.value,
            description=f"IAM role for {self.service_name} Fargate tasks",
            tags=helper.default_tags(self.service_name),
            managed_policy_arns=[self.EXECUTION_ROLE_POLICY],
            inline_policies=self.config.ecs_fargate.inline_policies,
            enable_instance_profile=False
        )).create_role()

    @staticmethod
    def create_default_ingress_rule() -> IngressRuleModel:
        return IngressRuleModel(
            from_port=8080,
            to_port=8080,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"]
        )
