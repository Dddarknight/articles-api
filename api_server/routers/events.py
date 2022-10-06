import httpx

from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from pymongo import MongoClient


router = APIRouter()

DB = "articles"
MSG_COLLECTION = "users_articles_views"


async def post_event(data):
    await httpx.AsyncClient().post('http://localhost:8000/events', json=data)
    return


@router.post("/events", response_class=HTMLResponse)
async def make_event(request: Request):
    response = await request.json()
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        msg_collection.insert_one({
            'object_id': response['object_id'],
            'type': response['type'],
            'date_time': response['date_time']})
    return


@router.get("/statistics")
async def get_statictics():
    statistics = []
    with MongoClient() as client:
        for document in client[DB][MSG_COLLECTION].find({}):
            statistics.append(document)
    print(statistics)
    return 1
