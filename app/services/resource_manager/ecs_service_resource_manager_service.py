from app.dto.create_ecs_service_request import CreateECSServiceRequest
from app.services.aws.ecs.aws_ecs_fargate_service import AwsECSFargate
from app.services.aws.iam import AwsIAMRole, AssumeRoleService
from app.services.aws.models import AwsIAMRoleModel
from app.services.aws.security_group import AwsSecurityGroup
from app.services.aws.security_group.aws_security_group_model import AwsSecurityGroupModel
from app.services.aws.security_group.ingress_rule_model import IngressRuleModel
from app.services.helper.pulumi_helper import PulumiHelper as helper
from app.services.resource_manager import ResourceManager


class ECSServiceResourceManagerService(ResourceManager):
    def __init__(self, config: CreateECSServiceRequest):
        self.config = config
        self.result = {}
        self.env = config.stack_name
        self.service_name = self.config.ecs_fargate.name

    def create_resources(self) -> dict:
        service = AwsECSFargate(self.config.ecs_fargate)
        if not self.config.ecs_fargate.vpc_security_group_ids:
            security_group = self.create_security_group()
            service.vpc_security_group_ids = [security_group["sg_id"]]
        if not self.config.ecs_fargate.task_role_arn:
            iam_role = self.create_iam_role()
            service.iam_role = iam_role["role_arn"]
        execution_role = self.create_execution_role()
        service.container_definitions = self.config.ecs_fargate.container_definitions
        service.execution_role_arn = execution_role["role_arn"]
        service.cluster_name = self.config.ecs_fargate.cluster_name
        service.create_fargate_service()
        self.result["service"] = service
        return self.result

    def create_security_group(self) -> dict | None:
        if not self.config.ecs_fargate.vpc_security_group_ids:
            security_group = self.default_sg()
            self.result["security_group"] = security_group
            return security_group
        if self.config.ingress or self.config.egress:
            return self.custom_sg()
        return None

    def custom_sg(self):
        custom_sg = AwsSecurityGroupModel(name=f"{self.config.ecs_fargate.name}",
                                          vpc_id=self.config.ecs_fargate.vpc_id,
                                          ingress=self.config.ecs_fargate.ingress,
                                          egress=self.config.ecs_fargate.egress)

    def default_sg(self):
        default_sg = AwsSecurityGroupModel(name=f"{self.config.ecs_fargate.name}-default",
                                           vpc_id=self.config.ecs_fargate.vpc_id,
                                           ingress=[self.create_default_ingress_rule()])
        return self.create_sg(default_sg)

    def create_execution_role(self):
        ecs_fargate_execution_role_model = AwsIAMRoleModel(
            enabled=True,
            name=f"{self.service_name}-ecs-execution",
            assume_role_policy=AssumeRoleService.ECS_TASK.value,
            description=f"IAM execution role for {self.service_name}-{self.env}",
            max_session_duration=3600,
            tags=helper.default_tags(self.service_name),
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
            ],
            inline_policies=None,
            enable_instance_profile=False
        )

        ecs_execution_role = AwsIAMRole(ecs_fargate_execution_role_model)
        return ecs_execution_role.create_role()

    @staticmethod
    def create_sg(model: AwsSecurityGroupModel):
        return AwsSecurityGroup(model).create_security_group()

    @staticmethod
    def create_default_ingress_rule():
        return IngressRuleModel(
            from_port=8080,
            to_port=8080,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"])

    def create_iam_role(self):
        iam_role = AwsIAMRoleModel(
            name=f"{self.service_name}-ecs-task",
            assume_role_policy=AssumeRoleService.ECS_TASK.value,
            description=f"IAM role for {self.service_name} Fargate tasks",
            tags=helper.default_tags(self.service_name),
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
            ],
            inline_policies=self.config.ecs_fargate.inline_policies,
            enable_instance_profile=False
        )
        return AwsIAMRole(iam_role).create_role()
