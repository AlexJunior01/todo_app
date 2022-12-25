from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.database import BaseModel, Session
from src.models.base_sql_model import BaseSQLModel


class User(BaseModel, BaseSQLModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    email = Column(String)
    last_name = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)

    tasks = relationship('Task', back_populates='user')
    projects = relationship('Project', back_populates='user')

    @classmethod
    def get_by_username(cls, db: Session, username: str) -> "User":
        return db.query(cls).filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> "User":
        return db.query(cls).filter_by(id=user_id).first()
