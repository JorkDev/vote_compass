# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# bring in Base & our app factory
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app

# ────────────────────────────────────────────────────
# ** IMPORT ALL MODELS ** so metadata knows about them
import app.db.models.user
import app.db.models.question
import app.db.models.party
import app.db.models.answer
import app.db.models.result
# ────────────────────────────────────────────────────

# Use a single in-memory SQLite DB across all connections
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # <-- ensures one DB for all sessions
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    # Create all tables once for the session
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client():
    app = create_app()
    # Override the FastAPI dependency to use our test DB sessions
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
