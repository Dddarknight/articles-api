from typing import Union

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: Union[str, None] = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
