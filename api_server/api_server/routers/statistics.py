from fastapi import APIRouter
from api_server.database import mongo_client, DB


router = APIRouter()


@router.get("/statistics")
async def get_statictics():
    cursor = mongo_client[DB].records.find({})
    statistics = []
    for document in await cursor.to_list(length=100):
        document['_id'] = str(document['_id'])
        statistics.append(document)
    return statistics
