from pydantic import BaseModel


class ListStackRequest(BaseModel):
    project_name: str
