import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from research_automation_system.app.main import app
from app.utils.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
   SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
   Base.metadata.create_all(bind=engine)
   try:
       db = TestingSessionLocal()
       yield db
   finally:
       db.close()
       Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
   def override_get_db():
       try:
           yield test_db
       finally:
           test_db.close()
   
   app.dependency_overrides[get_db] = override_get_db
   return TestClient(app)
