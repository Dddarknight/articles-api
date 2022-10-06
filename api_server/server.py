import uvicorn

from fastapi import FastAPI
from api_server.routers import users, articles, events
from api_server.database import database


app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(events.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8075)
