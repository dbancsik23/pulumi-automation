from pulumi import automation as auto

from app.services.pulumi.pulumi_commands import PulumiCommands
from app.services.pulumi.stack_operation import StackOperation


class PreviewStack(StackOperation):
    def execute(self, stack: auto.Stack, project_name: str, body: str):
        return stack.preview(on_output=print).change_summary


    def get_type(self) -> PulumiCommands:
        return PulumiCommands.PREVIEW
