from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ErrorMessage(BaseModel):
    message: str
    detail: Optional[str]
