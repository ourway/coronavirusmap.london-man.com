FROM python:3 AS base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Server
FROM base AS api-server

# Wait for database import and other stuff
ENTRYPOINT sleep 30 && alembic upgrade head && gunicorn main:app


## Worker
FROM base AS scheduler

ENTRYPOINT sleep 20 && celery -A tasks worker --loglevel=debug
