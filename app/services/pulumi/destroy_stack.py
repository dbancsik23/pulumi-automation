from pulumi import automation as auto

from app.services.pulumi.dto import PulumiCommands
from app.services.pulumi.stack_operation import StackOperation


class DestroyStack(StackOperation):
    def execute(self, stack: auto.Stack):
        destroy = stack.destroy(on_output=print)
        stack.workspace.remove_stack(stack.name)
        return destroy.summary

    def get_type(self) -> PulumiCommands:
        return PulumiCommands.DESTROY
