#!/usr/bin/python
# coding: utf-8
from flask import Flask, Blueprint
from flask_restful import Api, Resource, url_for
from typing import Any
import tasks
from core.database import init_db, db_session
from core.models import User


class Ping(Resource):
    def get(self):
        return {"result": "pong"}


class DbSetup(Resource):
    def post(self):
        init_db()
        return dict(result="ok")


class Populate(Resource):
    def post(self):
        tasks.get_postcodes_task.delay()
        return dict(result="ok")


def create_app(config: Any = None):
    """TODO: Docstring for create_app.
    :returns: TODO

    """
    app = Flask(__name__)
    app.config.update(config or {})
    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)
    api.add_resource(Ping, "/ping")
    api.add_resource(Populate, "/populate")
    api.add_resource(DbSetup, "/db_setup")
    app.register_blueprint(api_bp)
    return app
