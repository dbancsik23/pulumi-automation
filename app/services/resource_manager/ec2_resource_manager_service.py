from app.dto import CreateEC2Request
from app.services.helper.pulumi_helper import PulumiHelper as helper
from app.services.ec2 import AwsEC2Instance
from app.services.iam import AssumeRoleService, AwsIAMRole
from app.services.security_group import AwsSecurityGroup


class EC2ResourceManagerService:
    def __init__(self, config: CreateEC2Request):
        self.config = config
        self.result = {}

    def create_security_group(self) -> dict | None:
        if self.config.security_group and self.config.security_group.enabled:
            security_group = AwsSecurityGroup(**self.config.security_group.model_dump()).create_security_group()
            self.result["security_group"] = security_group
            return security_group
        return None

    def create_iam_role(self) -> dict | None:
        if self.config.iam_role and self.config.iam_role.enabled:
            iam_role = AwsIAMRole(**self.config.iam_role.model_dump())
            assume_role_policy = iam_role.generate_assume_role_policy(AssumeRoleService.EC2)
            iam_role.assume_role_policy = assume_role_policy
            role = iam_role.create_role()
            self.result["iam_role"] = role
            return role
        return None

    def create_ec2_instance(self, security_group=None, iam_role=None) -> dict:
        ec2_instance = AwsEC2Instance(**self.config.ec2_instance.model_dump())
        if security_group:
            ec2_instance.vpc_security_group_ids = [security_group["sg_id"]]
        ec2_instance.user_data_base64 = helper.read_user_data()
        if iam_role:
            ec2_instance.iam_instance_profile = iam_role["instance_profile_name"]["name"]
        instance = ec2_instance.create_instance()
        self.result["ec2_instance"] = instance
        return instance

    def create_resources(self) -> dict:
        try:
            security_group = self.create_security_group()
            iam_role = self.create_iam_role()
            self.create_ec2_instance(security_group=security_group, iam_role=iam_role)

            return self.result
        except Exception as e:
            print(f"Error during resource creation, message: {str(e)}")
            raise e
