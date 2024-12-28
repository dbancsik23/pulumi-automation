from typing import Optional, Dict, List

from pydantic import BaseModel


class ContainerDefinitionModel(BaseModel):
    container_name: str
    image: str
    port_mappings: Optional[List[Dict]] = None
    environment: Optional[List[Dict]] = None
    secrets: Optional[List[Dict]] = None
    log_configuration: Optional[Dict] = None
