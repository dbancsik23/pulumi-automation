from abc import ABC, abstractmethod


class ResourceManager(ABC):

    @abstractmethod
    def create_resources(self) -> dict:
        pass
