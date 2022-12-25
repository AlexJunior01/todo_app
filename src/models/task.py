from typing import List

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import BaseModel, Session
from src.models.base_sql_model import BaseSQLModel


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
    user = relationship('User', back_populates='tasks')

    @classmethod
    def get_all(cls, db: Session, user_id: int) -> List["Task"]:
        """
        Retrieve all items from database
        :param db: Database connection
        :return: List of Tasks Objects
        """
        return db.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def get_by_id(cls, db: Session, task_id: int, user_id: int) -> "Task":
        """
        Retrieve one task by id from database
        :param db: Database connection
        :param task_id: Task id used to search
        :return: Task Object
        """
        return db.query(cls).filter_by(id=task_id, user_id=user_id).first()

    @classmethod
    def get_by_ids(cls, db: Session, task_ids: List[int], user_id: int) -> List["Task"]:
        return db.query(cls).filter(cls.id.in_(task_ids)).filter_by(user_id=user_id).all()

    @classmethod
    def get_non_existent_ids(cls, db: Session, task_ids: List[int], user_id: int) -> List[int]:
        # TODO: try to change the implementation for some using set()
        ids_missing = []
        for task_id in task_ids:
            task = cls.get_by_id(db, task_id, user_id)
            if not task:
                ids_missing.append(task_id)

        return ids_missing
