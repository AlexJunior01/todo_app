from typing import Optional

from pydantic import BaseModel, Field


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

    class Config:
        orm_mode = True
