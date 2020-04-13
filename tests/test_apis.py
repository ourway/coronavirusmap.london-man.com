import pytest

from api import create_app
import json


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app.test_client()


def test_ping(app):
    res = app.get("/ping")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
    assert res.json["result"] == "pong"
