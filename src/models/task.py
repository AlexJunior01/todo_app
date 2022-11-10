from typing import List, Tuple, Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import SQLAlchemyError

from src.database import BaseModel, Session
from src.utils.database import update_object


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

    def save(self, db: Session) -> Tuple[bool, Optional[str]]:
        """
        Save a task instance in the database
        :param db: Database connection
        :return: Tuple(was_saved, error_description)
        """
        try:
            db.add(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def update(self, db: Session, update_args: dict):
        """
        Update a task instance
        :param db: Database connection
        :param update_args: Atributes to update
        :return: Tuple(was_saved, error_description)
        """
        try:
            update_object(db, self, update_args)
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def delete(self, db: Session):
        """
        Delete a task instance from the database
        :param db: Database connection
        :return:
        """
        try:
            db.delete(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)
