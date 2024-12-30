import json
import logging

from pulumi import automation as auto

from app.repository.stack_config_repo import *
from app.services.pulumi.pulumi_commands import PulumiCommands
from app.services.pulumi.stack_operation import StackOperation


class CreateStack(StackOperation):
    def execute(self, stack: auto.Stack, project_name: str, body: str):
        try:
            stack_up = stack.up(on_output=print).outputs
            self.manage_stack(project_name, stack.name, body, str(stack_up))
            return stack.up(on_output=print).outputs
        except Exception as e:
            logging.error(f"Failed to create stack, error: {str(e)}")
            raise e

    def get_type(self) -> PulumiCommands:
        return PulumiCommands.UP

    @staticmethod
    def manage_stack(project_name: str, stack_name: str, body: str = None, out: str = None):
        stack = get_by_project_and_stack(project_name, stack_name)
        if stack:
            stack.stack_configuration = json.dumps(body)
            update(id=stack.id, project_name=project_name, stack_name=stack_name,
                   stack_configuration=body, stack_output=json.dumps(out))
            return stack
        return add(project_name=project_name,
                   stack_name=stack_name,
                   stack_configuration=body,
                   stack_output=json.dumps(out))
