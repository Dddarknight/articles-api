from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api_server.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")
