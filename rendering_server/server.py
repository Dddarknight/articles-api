import sentry_sdk
import uvicorn
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from rendering_server.routers import users, articles

sentry_sdk.init(
    dsn="https://e98838ebed8648488f4d213fe3e28df5@o4504012217712640.ingest.sentry.io/4504012219744256",
    traces_sample_rate=1.0,
)
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

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
