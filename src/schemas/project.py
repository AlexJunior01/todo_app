from typing import Optional, List

from pydantic import BaseModel, Field

from src.schemas.task import TaskOutput


class ProjectInput(BaseModel):
    title: str
    description: Optional[str]
    finished: Optional[bool] = Field(default=False)


class ProjectUpdateInput(BaseModel):
    title: Optional[str]
    description: Optional[str]
    finished: Optional[bool] = Field(default=False)


class ProjectOutput(BaseModel):
    id: int
    title: str
    description: Optional[str]
    finished: Optional[bool] = Field(default=False)
    tasks: Optional[List[TaskOutput]] = Field(default=[])

    class Config:
        orm_mode = True
