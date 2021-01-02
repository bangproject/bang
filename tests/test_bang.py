"""Framework tests.

Test the App framework.
"""
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


def test_bang_test_client_can_send_requests(app, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @app.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT


def test_parameterized_route(app, client):
    @app.route("/hello/{name}")
    def hello(req, resp, name):
        resp.text = f"Hello, {name}"

    assert client.get("http://testserver/hello/Nathan").text == "Hello, Nathan"


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_based_handler_get(app, client):
    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = "get"

    assert client.get("http://testserver/book").text == "get"


def test_class_based_handler_post(app, client):
    @app.route("/person")
    class PersonResource:
        def post(self, req, resp):
            resp.text = "post"

    assert client.post("http://testserver/person").text == "post"

    # and undefined method raises
    with pytest.raises(AttributeError):
        client.get("http://testserver/person").text
