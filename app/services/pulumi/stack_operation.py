from abc import ABC, abstractmethod

from pulumi import automation as auto

from app.services.pulumi.pulumi_commands import PulumiCommands


class StackOperation(ABC):
    @abstractmethod
    def execute(self, stack: auto.Stack):
        pass

    @abstractmethod
    def get_type(self) -> PulumiCommands:
        pass
