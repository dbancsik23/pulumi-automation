from app.services.pulumi.pulumi_commands import PulumiCommands
from app.services.pulumi.pulumi_stack_service import PulumiStackService


def handle_stack_operation(stack_name: str, project_name: str, action: PulumiCommands, program, body: str):
    stack_service = PulumiStackService(
        stack_name=stack_name,
        project_name=project_name,
        program_name=program

    )
    return stack_service.execute_stack_operation(action, project_name, body)
