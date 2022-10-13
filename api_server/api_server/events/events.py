from fastapi import APIRouter
from dotenv import load_dotenv
from api_server.api_server.database import mongo_client, DB


load_dotenv()

router = APIRouter()


async def make_event(data):
    mongo_client[DB].records.insert_one({
        'object_id': data['object_id'],
        'object': data['object'],
        'type': data['type'],
        'date_time': data['date_time']})
    return
