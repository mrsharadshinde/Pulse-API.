import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.config import settings
from app.Database.database import get_db, Base
from app.utils import limiter

limiter.enabled = False
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

#---------------------------- for POST CRUD & Voting unit Test
@pytest.fixture
def token(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    return res.json()["access_token"]


@pytest.fixture
def authorized_client(client, token):
    # 1. Create a completely separate fake browser
    new_client = TestClient(app)

    # 2. Attach the token ONLY to this new browser
    new_client.headers = {
        **new_client.headers,
        "Authorization": f"Bearer {token}"
    }

    return new_client

@pytest.fixture
def test_post(authorized_client):
    res = authorized_client.post(
        "/posts/", json={
            "title": "Test Post for Voting",
            "content": "This post is ready to be voted on.",
            "published": True
        })
    return res.json()