FROM python:3 AS base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Server
FROM base AS api-server

CMD [ "python", "./run.py" ]


## Worker
FROM base AS scheduler

ENTRYPOINT celery -A tasks worker --loglevel=debug

