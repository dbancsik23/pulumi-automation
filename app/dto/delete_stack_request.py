from typing import Optional

from pydantic import BaseModel


class DeleteStackRequest(BaseModel):
    project_name: str
    stack_name: str
