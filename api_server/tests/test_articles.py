import pytest
import asynctest
from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_server.database import Base
from api_server.server import app
from api_server.dependencies import get_db
from api_server.routers.users import ACCESS_TOKEN_EXPIRE_MINUTES
from api_server.tests.utils import get_test_data
from api_server.tests.test_users import test_data_users
from api_server.tokens.token import create_access_token
import api_server.routers.articles


test_data_articles = get_test_data('articles.json')

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


def test_create_and_get_article(test_db, monkeypatch):
    user_data = test_data_users["users"]["user1"]
    user = client.post('/sign-up', json=user_data)

    article_data = test_data_articles["articles"]["article1"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.json()['username']}, expires_delta=access_token_expires
    )

    article = client.post('/users/1/articles/create',
                          json=article_data,
                          headers={"Authorization": f"Bearer {access_token}"})
    assert article.json()['title'] == article_data['title']
    assert article.json()['content'] == article_data['content']
    
    fake_function = asynctest.CoroutineMock(api_server.routers.articles.post_event)
    monkeypatch.setattr(api_server.routers.articles, 'post_event', fake_function)
    article = client.get('/users/1/articles/1',
                          headers={"Authorization": f"Bearer {access_token}"})
    assert article.json()['title'] == article_data['title']
    assert article.json()['content'] == article_data['content']


def test_update_article_by_author(test_db):
    user_data = test_data_users["users"]["user1"]
    user = client.post('/sign-up', json=user_data)

    article_data_initial = test_data_articles["articles"]["article1"]
    article_data_changed = test_data_articles["articles"]["article2"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.json()['username']}, expires_delta=access_token_expires
    )

    client.post('/users/1/articles/create',
                json=article_data_initial,
                headers={"Authorization": f"Bearer {access_token}"})
    article = client.put('/users/1/articles/1',
                         json=article_data_changed,
                         headers={"Authorization": f"Bearer {access_token}"})
    assert article.json()['title'] == article_data_changed['title']
    assert article.json()['content'] == article_data_changed['content']


def test_update_article_by_not_author(test_db):
    user1_data = test_data_users["users"]["user1"]
    user2_data = test_data_users["users"]["user2"]
    user1 = client.post('/sign-up', json=user1_data)
    user2 = client.post('/sign-up', json=user2_data)

    article_data_initial = test_data_articles["articles"]["article1"]
    article_data_changed = test_data_articles["articles"]["article2"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token1 = create_access_token(
        data={"sub": user1.json()['username']}, expires_delta=access_token_expires
    )

    client.post('/users/1/articles/create',
                json=article_data_initial,
                headers={"Authorization": f"Bearer {access_token1}"})
    access_token2 = create_access_token(
        data={"sub": user2.json()['username']}, expires_delta=access_token_expires
    )
    response = client.put('/users/1/articles/1',
                          json=article_data_changed,
                          headers={"Authorization": f"Bearer {access_token2}"})
    assert response.status_code == 404


def test_delete_article(test_db):
    user_data = test_data_users["users"]["user1"]
    user = client.post('/sign-up', json=user_data)

    article_data = test_data_articles["articles"]["article1"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.json()['username']}, expires_delta=access_token_expires
    )

    client.post('/users/1/articles/create',
                json=article_data,
                headers={"Authorization": f"Bearer {access_token}"})
    client.delete('/users/1/articles/1',
                  headers={"Authorization": f"Bearer {access_token}"})
    response = client.get('/users/1/articles/1',
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404
