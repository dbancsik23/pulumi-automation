from pulumi import automation as auto

from app.services.pulumi.pulumi_commands import PulumiCommands
from app.services.pulumi.stack_operation import StackOperation


class CreateStack(StackOperation):
    def execute(self, stack: auto.Stack):
        return stack.up(on_output=print).outputs

    def get_type(self) -> PulumiCommands:
        return PulumiCommands.UP
