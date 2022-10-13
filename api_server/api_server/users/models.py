from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from api_server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_moderator = Column(Boolean, default=True)

    articles = relationship("Article", back_populates="author")
