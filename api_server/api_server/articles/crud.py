from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api_server.api_server import articles


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(articles.models.Article).offset(skip).limit(limit).all()


def get_article(db: Session, id: int):
    return db.query(
        articles.models.Article).filter(
            articles.models.Article.id == id).first()


def create_article(db: Session,
                   article: articles.schemas.ArticleCreate,
                   user_id: int):
    db_article = articles.models.Article(**article.dict(), author_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session,
                   article_id: int,
                   new_article_data: Union[BaseModel, Dict[str, Any]]):
    db_article = get_article(db, article_id)
    db_article_data = jsonable_encoder(db_article)
    if isinstance(new_article_data, dict):
        update_data = new_article_data
    else:
        update_data = new_article_data.dict(exclude_unset=True)
    for field in db_article_data:
        if field in update_data:
            setattr(db_article, field, update_data[field])
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session,
                   article_id: int):
    db_article = get_article(db, article_id)
    db.delete(db_article)
    db.commit()
    return db_article
