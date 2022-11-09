import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config

from src.app import app
from src.config import DB_TEST_URL, DB_CONNECTION_URL
from src.database import get_db, BaseModel
from src.utils.database import run_migration


test_engine = create_engine(DB_TEST_URL)
TestSession = sessionmaker(bind=test_engine)


def override_get_db():
    try:
        db = TestSession()
        yield db
    finally:
        db.close()


@pytest.fixture
def web_client():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def db_client():
    BaseModel.metadata.drop_all(bind=test_engine)
    BaseModel.metadata.create_all(bind=test_engine)
    session = TestSession()
    yield session
    session.close()


@pytest.fixture
def valid_task():
    return {
        "title": "Go to the market",
        "description": "Buy beer and fruits",
        "priority": 1,
        "is_complete": False
    }


@pytest.fixture
def invalid_task():
    return {
        "description": "Buy beer and fruits",
        "priority": 1,
        "is_complete": False
    }
