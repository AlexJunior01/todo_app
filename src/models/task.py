from typing import List

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
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db: Session, task_id: int) -> "Task":
        return db.query(cls).filter_by(id=task_id).first()

    def save(self, db: Session):
        try:
            db.add(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def update(self, db: Session, update_args: dict):
        try:
            update_object(db, self, update_args)
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def delete(self, db: Session):
        try:
            db.delete(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)
