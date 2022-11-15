from typing import List, Tuple, Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from src.database import BaseModel, Session
from src.models.task import Task
from src.utils.database import update_object


class Project(BaseModel):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String, default="")
    finished = Column(Boolean, default=False)

    tasks = relationship('Task', back_populates='project')

    @classmethod
    def get_all(cls, db: Session) -> List["Project"]:
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db: Session, project_id: int) -> "Project":
        return db.query(cls).filter_by(id=project_id).first()

    def add_tasks(self, db: Session, tasks: List[Task]):
        try:
            for task in tasks:
                self.tasks.append(task)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def remove_tasks(self, db: Session, tasks: List[Task]):
        try:
            for task in tasks:
                self.tasks.remove(task)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def save(self, db: Session):
        """
        Save a project instance in the database
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
        Update a project instance
        :param db: Database connection
        :param update_args: Atributes to update
        :return: Tuple(was_updated, error_description)
        """
        try:
            update_object(db, self, update_args)
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def delete(self, db: Session):
        """
        Delete a project instance
        :param db: Database connection
        :return:
        """
        try:
            db.delete(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)
