from enum import Enum


class AssumeRoleService(Enum):
    EC2 = "ec2.amazonaws.com"
    LAMBDA = "lambda.amazonaws.com"
    ECS_TASK = "ecs-tasks.amazonaws.com"
