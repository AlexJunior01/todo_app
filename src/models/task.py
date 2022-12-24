from typing import List, Tuple, Optional

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from src.database import BaseModel, Session
from src.models.base_sql_model import BaseSQLModel
from src.utils.database import update_object


class Task(BaseModel, BaseSQLModel):
    """
    Mapping class for table task
    """

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String, default="")
    priority = Column(Integer, nullable=False)
    is_complete = Column(Boolean, nullable=False, default=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    project = relationship('Project', back_populates='tasks')
    user = relationship('Users', back_populates='tasks')

    @classmethod
    def get_all(cls, db: Session) -> List["Task"]:
        """
        Retrieve all items from database
        :param db: Database connection
        :return: List of Tasks Objects
        """
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db: Session, task_id: int) -> "Task":
        """
        Retrieve one task by id from database
        :param db: Database connection
        :param task_id: Task id used to search
        :return: Task Object
        """
        return db.query(cls).filter_by(id=task_id).first()

    @classmethod
    def get_by_ids(cls, db: Session, task_ids: List[int]) -> List["Task"]:
        return db.query(cls).filter(cls.id.in_(task_ids)).all()

    @classmethod
    def get_non_existent_ids(cls, db: Session, task_ids: List[int]) -> List[int]:
        ids_missing = []
        for task_id in task_ids:
            task = cls.get_by_id(db, task_id)
            if not task:
                ids_missing.append(task_id)

        return ids_missing
