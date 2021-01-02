from bang.api import BangAPI

import pytest


def test_basic_route_adding(app):
    @app.route("/basic")
    def home(req, resp):
        resp.text = "YOLO"


def test_no_duplicate_routes(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AttributeError):
        @app.route("/home")
        def home2(req, resp):
            resp.text = "Not again"
