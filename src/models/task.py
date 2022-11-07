from sqlalchemy import Column, Integer, String, Boolean

from src.database import BaseModel, Session


class Task(BaseModel):
    """
    Mapping class for table task
    """

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String, default="")
    priority = Column(Integer, nullable=False)
    is_complete = Column(Boolean, nullable=False, default=False)
