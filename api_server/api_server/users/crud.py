from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api_server.api_server import users
from api_server.api_server.users.schemas import UserCreate


def get_user(db: Session, id: int):
    return db.query(
        users.models.User).filter(users.models.User.id == id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(
        users.models.User).filter(
            users.models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(
        users.models.User).filter(
            users.models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(
        users.models.User).offset(skip).limit(limit).all()


def get_moderators(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(
        users.models.User).filter(
            users.models.User.is_moderator is True).offset(
                skip).limit(limit).all())


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session,
                      username: str,
                      password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session,
                user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = users.models.User(username=user.username,
                                email=user.email,
                                full_name=user.full_name,
                                is_moderator=False,
                                hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session,
                user_id: int,
                new_user_data: Union[BaseModel, Dict[str, Any]]):
    db_user = get_user(db, user_id)
    db_user_data = jsonable_encoder(db_user)
    if isinstance(new_user_data, dict):
        update_data = new_user_data
    else:
        update_data = new_user_data.dict(exclude_unset=True)
    for field in db_user_data:
        if field in update_data:
            if field == 'password':
                update_data[field] = get_password_hash(update_data[field])
            setattr(db_user, field, update_data[field])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session,
                user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user
