import os
import motor.motor_asyncio

import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()

MONGODB_URL = os.getenv('MONGODB_URL')

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

DB = 'articles'

MSG_COLLECTION = "users_articles_views"
