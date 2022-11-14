from typing import Optional

from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6)
    is_complete: Optional[bool] = Field(default=False)


class TaskUpdateInput(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int] = Field(gt=0, lt=6)
    is_complete: Optional[bool]


class TaskOutput(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6)
    is_complete: Optional[bool] = Field(default=False)
    project_id: Optional[int] = Field(default=None)

    class Config:
        orm_mode = True
