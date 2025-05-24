# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app

# 1. In-memory SQLite
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# 2. Create all tables once per test session
@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 3. Override get_db to use the test DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. TestClient with dependency override
@pytest.fixture()
def client(monkeypatch):
    app = create_app()
    monkeypatch.setattr("app.db.session.get_db", override_get_db)
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
