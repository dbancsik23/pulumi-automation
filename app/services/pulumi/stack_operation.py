from abc import ABC, abstractmethod

from pulumi import automation as auto

from app.services.pulumi.pulumi_commands import PulumiCommands


class StackOperation(ABC):
    @abstractmethod
    def execute(self, stack: auto.Stack, project_name: str, body: str):
        pass

    @abstractmethod
    def get_type(self) -> PulumiCommands:
        pass
