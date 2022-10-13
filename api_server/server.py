import os
import uvicorn
import databases

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_server.api_server.routers import users, articles, statistics
from api_server.api_server.database import engine
from api_server.api_server.users import models as users_models
from api_server.api_server.articles import models as articles_models
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event('startup')
async def startup():
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
    database = databases.Database(SQLALCHEMY_DATABASE_URL)
    await database.connect()
    users_models.Base.metadata.create_all(bind=engine)
    articles_models.Base.metadata.create_all(bind=engine)


@app.on_event('shutdown')
async def shutdown():
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
    database = databases.Database(SQLALCHEMY_DATABASE_URL)
    await database.disconnect()


app.include_router(users.router)
app.include_router(articles.router)
app.include_router(statistics.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
