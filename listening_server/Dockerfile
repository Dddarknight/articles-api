FROM tiangolo/uvicorn-gunicorn-fastapi

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /listening_server/.

CMD uvicorn listening_server.server:app --host 0.0.0.0 --port 3001