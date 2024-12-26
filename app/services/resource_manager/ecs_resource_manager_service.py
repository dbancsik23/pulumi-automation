from app.dto.create_ecs_request import CreateECSRequest


class ECSResourceManagerService:
    def __init__(self, config: CreateECSRequest):
        self.config = config
        self.result = {}

    def create_resources(self) -> dict:
        pass
