#!/usr/bin/python
# coding: utf-8
from flask import Flask, Blueprint
from flask_restful import Api, Resource, url_for
from tasks import add

app = Flask(__name__)
api_bp = Blueprint("api", __name__)
api = Api(api_bp)


class TodoItem(Resource):
    def get(self, a, b):
        task = add.delay(a, b)
        return {"task": f"Added {a} and {b}"}


api.add_resource(TodoItem, "/api/v1/scheduler/add/<int:a>/<int:b>")
app.register_blueprint(api_bp)
