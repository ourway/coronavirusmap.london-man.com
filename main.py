#!/usr/bin/python
# coding: utf-8
from api import create_app
from core.database import db_session

app = create_app()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
