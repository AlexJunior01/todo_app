from typing import List, Tuple, Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from src.database import BaseModel, Session
from src.models.base_sql_model import BaseSQLModel
from src.models.task import Task
from src.utils.database import update_object


class Project(BaseModel, BaseSQLModel):
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
