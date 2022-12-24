from sqlalchemy import Column, Integer, String, Boolean

from src.database import BaseModel
from src.models.base_sql_model import BaseSQLModel


class Users(BaseModel, BaseSQLModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    email = Column(String)
    last_name = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)
