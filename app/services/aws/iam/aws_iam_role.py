from typing import Optional, List, Dict

import pulumi
import pulumi_aws as aws

from app.services.aws.iam import AssumeRoleService
from app.services.aws.models.aws_iam_role_model import AwsIAMRoleModel
from app.services.helper.pulumi_helper import PulumiHelper as helper


class AwsIAMRole:
    def __init__(self, model: AwsIAMRoleModel):
        self.enabled = model.enabled
        self.env = pulumi.get_stack()
        self.name: str = f"{model.name}-{self.env}-role"
        self.assume_role_policy: AssumeRoleService = AssumeRoleService(model.assume_role_policy)
        self.description: Optional[str] = model.description
        self.max_session_duration: Optional[int] = model.max_session_duration or 3600
        self.tags: Dict[str, str] = model.tags or helper.default_tags(self.name)
        self.managed_policy_arns: List[str] = model.managed_policy_arns or []
        self.inline_policies: Dict[str, str] = model.inline_policies or {}
        self.role: Optional[aws.iam.Role] = None
        self.enable_instance_profile: bool = model.enable_instance_profile

    def create_role(self):

        self.role = aws.iam.Role(
            resource_name=self.name,
            assume_role_policy=self.generate_assume_role_policy(self.assume_role_policy),
            description=self.description,
            max_session_duration=self.max_session_duration,
            tags=self.tags
        )

        for idx, policy_arn in enumerate(self.managed_policy_arns, start=1):
            aws.iam.RolePolicyAttachment(
                f"{self.name}-managed-policy-{idx}",
                role=self.role.name,
                policy_arn=policy_arn
            )

        for policy_name, policy_document in self.inline_policies.items():
            aws.iam.RolePolicy(
                f"{self.name}-{policy_name}",
                role=self.role.name,
                policy=policy_document
            )

        pulumi.export(f"{self.name}_role_name", self.role.name)
        pulumi.export(f"{self.name}_role_arn", self.role.arn)
        role_name = self.role.name.apply(lambda name: {"name": name})["name"]
        role_arn = self.role.arn.apply(lambda arn: {"arn": arn})["arn"]

        if self.enable_instance_profile:
            instance_profile = self.create_instance_profile()
            instance_profile_name = instance_profile.name.apply(lambda name: {"name": name})
            instance_profile_arn = instance_profile.arn.apply(lambda arn: {"arn": arn})
            return self.generate_output(role_name, role_arn, instance_profile_name, instance_profile_arn)
        return self.generate_output(role_name, role_arn)

    def create_instance_profile(self):
        if not self.role:
            raise ValueError("Role must be created before creating an instance profile.")

        instance_profile = aws.iam.InstanceProfile(
            f"{self.name}-instance-profile",
            role=self.role.name,
            name=f"{self.name}-instance-profile"
        )

        pulumi.export(f"{self.name}_instance_profile_name", instance_profile.name)
        pulumi.export(f"{self.name}_instance_profile_arn", instance_profile.arn)

        return instance_profile

    @staticmethod
    def generate_output(role_name, role_arn, instance_profile_name="", instance_profile_arn=""):
        return {
            "role_name": role_name,
            "role_arn": role_arn,
            "instance_profile_name": instance_profile_name,
            "instance_profile_arn": instance_profile_arn
        }

    def generate_assume_role_policy(self, resource: AssumeRoleService):
        if self.assume_role_policy:
            return {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": resource.value},
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
        return None
