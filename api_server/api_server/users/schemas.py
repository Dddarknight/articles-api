from typing import List, Union

from pydantic import BaseModel

from api_server.api_server.articles.schemas import Article


class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    articles: List[Article] = []

    class Config:
        orm_mode = True
