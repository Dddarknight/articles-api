from typing import List
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api_server.api_server import dependencies, articles
from api_server.api_server.tokens.models import Token
from api_server.api_server.tokens.token import create_access_token
from api_server.api_server.users import schemas, crud
from api_server.api_server.users import models as users_models
from api_server.api_server.users.schemas import User
from api_server.api_server.events.events import make_event


router = APIRouter()


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/token", response_model=Token)
async def login_for_access_token(
        db: Session = Depends(dependencies.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/", response_model=List[schemas.User])
async def read_users(db: Session = Depends(dependencies.get_db),
                     skip: int = 0,
                     limit: int = 100):
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(*,
                    user_id: int,
                    db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    event_data = {'object_id': db_user.id,
                  'object': 'user',
                  'type': 'view',
                  'date_time': str(datetime.now())}
    await make_event(event_data)
    return db_user


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
        user: users_models.User = Depends(dependencies.get_current_user)):
    return user


@router.get("/users/me/articles/")
async def read_own_articles(
        user: users_models.User = Depends(dependencies.get_current_user)):
    return user.articles


@router.post('/sign-up', response_model=schemas.User)
async def create_user(*,
                      user: schemas.UserCreate,
                      db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered.')
    return crud.create_user(db=db, user=user)


@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(*,
                      user_id: int,
                      db: Session = Depends(dependencies.get_db),
                      new_user_data: schemas.UserCreate,
                      user: User = Depends(dependencies.get_current_user)):
    db_user = crud.get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == user_id:
        return crud.update_user(db=db,
                                user_id=user_id,
                                new_user_data=new_user_data)
    raise HTTPException(status_code=404, detail="Can't update another user")


@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int,
                      db: Session = Depends(dependencies.get_db),
                      user: User = Depends(dependencies.get_current_user),):
    db_user = crud.get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == user_id:
        for article in user.articles:
            articles.crud.delete_article(db=db,
                                         article_id=article.id)
        return crud.delete_user(db=db,
                                user_id=user_id)
    raise HTTPException(status_code=404, detail="Can't delete another user")


@router.get("/moderators/", response_model=List[schemas.User])
async def read_moderators(db: Session = Depends(dependencies.get_db),
                          skip: int = 0,
                          limit: int = 100):
    return crud.get_moderators(db=db, skip=skip, limit=limit)
