import base64
from typing import Optional, List, Dict

import pulumi
import pulumi_aws as aws
from pulumi_aws.ec2 import InstanceLaunchTemplateArgs

from app.services.aws.models import AwsEC2Model
from app.services.helper.pulumi_helper import PulumiHelper as helper


class AwsEC2Instance:
    def __init__(self, model: AwsEC2Model):
        self.enabled = model.enabled
        self.name: str = f"{model.name}"
        self.instance_type: str = model.instance_type
        self.ami_id: str = model.ami_id
        self.vpc_security_group_ids: List[str] = model.vpc_security_group_ids or []
        self.subnet_id: Optional[str] = model.subnet_id
        self.key_name: Optional[str] = model.key_name
        self.default_tags = helper.default_tags(self.name)
        self.tags: Dict[str, str] = model.tags or self.default_tags
        self.additional_volumes: Optional[List[Dict[str, str]]] = model.additional_volumes or []
        self.launch_template: InstanceLaunchTemplateArgs = model.launch_template
        self.user_data: str = model.user_data
        self._user_data_base64: str = model.user_data_base64
        self.private_ip: str = model.private_ip
        self.availability_zone: str = model.availability_zone
        self.iam_instance_profile: str = model.iam_instance_profile
        self.associate_public_ip_address: bool = model.associate_public_ip_address

    @property
    def user_data_base64(self):
        return self._user_data_base64

    @user_data_base64.setter
    def user_data_base64(self, user_data):
        self._user_data_base64 = self.encode(user_data)

    def create_instance(self):
        if not self.enabled:
            pulumi.log.info(f"Instance creation skipped for {self.name} as it is disabled.")
            return
        instance = aws.ec2.Instance(
            self.name,
            instance_type=self.instance_type,
            ami=self.ami_id,
            vpc_security_group_ids=self.vpc_security_group_ids,
            subnet_id=self.subnet_id,
            key_name=self.key_name,
            tags=self.tags,
            associate_public_ip_address=self.associate_public_ip_address,
            launch_template=self.launch_template,
            user_data=self.user_data,
            user_data_base64=self._user_data_base64,
            private_ip=self.private_ip,
            availability_zone=self.availability_zone,
            iam_instance_profile=self.iam_instance_profile

        )

        for idx, volume in enumerate(self.additional_volumes, start=1):
            aws.ec2.VolumeAttachment(
                f"{self.name}-vol-{idx}",
                instance_id=instance.id,
                volume_id=volume["volume_id"],
                device_name=volume["device_name"],
            )

        pulumi.export(f"{self.name}_instance_id", instance.id)
        pulumi.export(
            f"{self.name}_details",
            instance.id.apply(lambda id: f"Instance {self.name} created with ID: {id}")
        )

        pulumi.export(f"{self.name}_instance_id", instance.id)
        pulumi.export(f"{self.name}_public_ip", instance.public_ip)

    @staticmethod
    def encode(user_data):
        if user_data:
            return base64.b64encode(user_data.encode("utf-8")).decode("utf-8")
