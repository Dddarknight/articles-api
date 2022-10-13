FROM tiangolo/uvicorn-gunicorn-fastapi

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /api_server/.

CMD uvicorn api_server.server:app --host 0.0.0.0 --port 8080