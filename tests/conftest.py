import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.config import settings
from app.Database.database import get_db, Base

#1. Create the Test Database URL
TEST_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#2 The Database Fixture: Clears and recreates table before EVERY test
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)  #Destry old data
    Base.metadata.create_all(bind=engine) # Create Fresh tables
    db = TestingSessionLocal()
    try:
        yield  db
    finally:
        db.close()

#3. The client Fixture: Overrides the API to use the test Database
@pytest.fixture()
def client(session):
    def overrides_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrides_get_db
    yield TestClient(app)


#------------------------for login testing-------------------
@pytest.fixture
def test_user(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "username": "test_user",
        "password": "password123"
    }

    # Register the user
    res = client.post("/users/", json=user_data)

    # Extract the user data from the response
    new_user = res.json()

    # Attach the raw password back onto the dictionary so our login tests can use it
    new_user['password'] = user_data['password']

    return new_user
