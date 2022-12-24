from typing import Optional

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    username: str
    first_name: str
    email: str
    last_name: str
    password: str
    active: bool


class UserOutPut(BaseModel):
    id: int
    username: str
    first_name: str
    email: str
    last_name: str

    class Config:
        orm_mode = True
