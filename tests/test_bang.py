from bang.api import BangAPI

import pytest


@pytest.fixture
def app():
    return BangAPI()


def test_no_duplicate_routes(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AttributeError):
        @app.route("/home")
        def home2(req, resp):
            resp.text = "Not again"

    
