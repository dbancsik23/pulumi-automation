import logging

from fastapi import HTTPException
from pulumi import automation as auto

from app.services.pulumi.create_stack import CreateStack
from app.services.pulumi.destroy_stack import DestroyStack
from app.services.pulumi.dto import PulumiCommands
from app.services.pulumi.preview_stack import PreviewStack


class PulumiStackService:
    def __init__(self, stack_name: str, project_name: str, program_name, region: str = "eu-central-1"):
        self.stack_name = stack_name
        self.project_name = project_name
        self.program_name = program_name
        self.region = region
        self.instances = [CreateStack(), PreviewStack(), DestroyStack()]
        self.ensure_plugins()

    @staticmethod
    def ensure_plugins():
        ws = auto.LocalWorkspace()
        ws.install_plugin("aws", "v4.0.0")

    def create_or_select_stack(self) -> auto.Stack:
        try:
            stack = auto.create_or_select_stack(stack_name=self.stack_name,
                                                project_name=self.project_name,
                                                program=self.program_name)
            stack.set_config("aws:region", auto.ConfigValue(self.region))
            logging.info(f"New stack '{self.stack_name}' created for project '{self.project_name}'")
            return stack
        except auto.StackAlreadyExistsError:
            raise HTTPException(status_code=404, detail=f"stack '{self.stack_name}' already exists")
        except auto.ConcurrentUpdateError:
            raise HTTPException(status_code=409, detail=f"stack '{self.stack_name}' is currently being updated")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"stack '{self.stack_name}' could not be created, with {str(e)}")

    def execute_stack_operation(self, stack_operation: PulumiCommands):
        try:
            stack = self.create_or_select_stack()
            for instance in self.instances:
                if instance.get_type() == stack_operation:
                    logging.info(
                        f"executing stack operation '{stack_operation}', for project '{self.project_name}' and stack '{self.stack_name}'")
                    return instance.execute(stack)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"stack operation '{stack_operation}' failed to execute, with {str(e)}")
