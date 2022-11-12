from typing import List, Tuple, Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from src.database import BaseModel, Session
from src.utils.database import update_object


class Project(BaseModel):
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String, default="")
    finished = Column(Boolean, default=False)

    tasks = relationship('Task', back_populates='tasks')
