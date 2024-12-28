from app.services.aws.ec2 import AwsEC2Instance
from app.services.aws.ecs.aws_ecs_fargate_service import AwsECSFargate
from app.services.aws.iam import AwsIAMRole
from app.services.aws.models import AwsIAMRoleModel, AwsEcsFargateModel, AwsEC2Model
from app.services.aws.security_group import AwsSecurityGroup
from app.services.aws.security_group.aws_security_group_model import AwsSecurityGroupModel


class ResourceFactory:
    RESOURCE_TYPE_MAPPING = {
        AwsSecurityGroupModel: AwsSecurityGroup,
        AwsEcsFargateModel: AwsECSFargate,
        AwsIAMRoleModel: AwsIAMRole,
        AwsEC2Model: AwsEC2Instance
    }

    @staticmethod
    def build(resource_model_instance, *args, **kwargs):
        resource_type = type(resource_model_instance)
        resource_cls = ResourceFactory.RESOURCE_TYPE_MAPPING.get(resource_type)
        if not resource_cls:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        return resource_cls(resource_model_instance)
