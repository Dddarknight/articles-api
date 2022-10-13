import pytest
import asynctest
from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_server.server import app
from api_server.database import Base
from api_server.api_server.dependencies import get_db
from api_server.api_server.routers import users
from api_server.api_server.routers.users import ACCESS_TOKEN_EXPIRE_MINUTES
from api_server.tests.utils import get_test_data
from api_server.api_server.tokens.token import create_access_token


test_data_users = get_test_data('users.json')

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user(test_db):
    data = test_data_users["users"]["user1"]
    user = client.post('/sign-up',
                       json=data)
    assert user.json()['username'] == data['username']
    assert user.json()['email'] == data['email']
    assert user.json()['full_name'] == data['full_name']


def test_get_user(test_db, monkeypatch):
    data = test_data_users["users"]["user1"]
    client.post('/sign-up', json=data)
    fake_function = asynctest.CoroutineMock(
        users.make_event)
    monkeypatch.setattr(
        users, 'make_event', fake_function)
    user = client.get('/users/1')
    assert user.json()['username'] == data['username']
    assert user.json()['email'] == data['email']
    assert user.json()['full_name'] == data['full_name']


def test_update_user(test_db):
    data_initial = test_data_users["users"]["user1"]
    user = client.post('/sign-up', json=data_initial)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.json()['username']},
        expires_delta=access_token_expires
    )
    print(access_token)
    data_changed = test_data_users["users"]["user2"]
    user = client.put('/users/1',
                      json=data_changed,
                      headers={"Authorization": f"Bearer {access_token}"})
    assert user.json()['username'] == data_changed['username']
    assert user.json()['email'] == data_changed['email']
    assert user.json()['full_name'] == data_changed['full_name']


def test_delete_user(test_db):
    data = test_data_users["users"]["user1"]
    user = client.post('/sign-up', json=data)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.json()['username']},
        expires_delta=access_token_expires
    )
    client.delete('/users/1',
                  headers={"Authorization": f"Bearer {access_token}"})
    response = client.get('/users/1')
    assert response.status_code == 404
