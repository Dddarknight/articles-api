import uvicorn

from fastapi import FastAPI, Request
from listening_server.listener import Listener

app = FastAPI()


@app.get('/')
async def index(request: Request):
    listener = Listener()
    listener.listen_to_queue(exchange='registration', queue='email_queue')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
