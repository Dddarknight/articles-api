import os
import sentry_sdk
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from rendering_server.routers import users, articles
from rendering_server.utils import templates
from dotenv import load_dotenv


load_dotenv()

DSN = os.getenv('DSN')

sentry_sdk.init(
    dsn=DSN,
    traces_sample_rate=1.0,
)
app = FastAPI()

app.include_router(users.router)
app.include_router(articles.router)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    if request.cookies.get('message'):
        response = templates.TemplateResponse(
            "index.html",
            {"request": request,
             "message": request.cookies['message']})
        response.delete_cookie('message')
    else:
        response = templates.TemplateResponse(
            "index.html",
            {"request": request})
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
