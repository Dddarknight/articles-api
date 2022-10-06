from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_server import dependencies
from api_server.articles import crud, schemas
from api_server.users.schemas import User
from api_server.routers.events import post_event


router = APIRouter()


@router.post("/users/{user_id}/articles/create",
             response_model=schemas.Article)
async def create_article(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    article: schemas.ArticleCreate,
    user: User = Depends(dependencies.get_current_user),
):
    if user.id == user_id:
        article = crud.create_article(db=db, article=article, user_id=user_id)
        return article
    raise HTTPException(
        status_code=404, detail="Can't create another user's article")


@router.get("/users/{user_id}/articles/{article_id}",
            response_model=schemas.Article)
async def read_article(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    article_id: int
):
    article = crud.get_article(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    event_data = {'object_id': article_id,
                  'type': 'view',
                  'date_time': str(datetime.now())}
    await post_event(event_data)
    return article


@router.put("/users/{user_id}/articles/{article_id}",
            response_model=schemas.Article)
async def update_article(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    article_id: int,
    new_article_data: schemas.ArticleCreate,
    user: User = Depends(dependencies.get_current_user),
):
    article = crud.get_article(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if user.id == user_id:
        return crud.update_article(db=db,
                                   article_id=article_id,
                                   new_article_data=new_article_data)
    raise HTTPException(
        status_code=404, detail="Can't update another user's article")


@router.delete("/users/{user_id}/articles/{article_id}",
               response_model=schemas.Article)
async def delete_article(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    article_id: int,
    user: User = Depends(dependencies.get_current_user),
):
    article = crud.get_article(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if user.id == user_id:
        return crud.delete_article(db=db,
                                   article_id=article_id)
    raise HTTPException(
        status_code=404, detail="Can't update another user's article")
