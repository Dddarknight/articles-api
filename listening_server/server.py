import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from listening_server.listener import Listener

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    listener = Listener()
    listener.listen_to_queue(exchange='registration', queue='email_queue')
    html_content = """
    <html>
        <head>
            <title>!</title>
        </head>
        <body>
            <h1>!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
