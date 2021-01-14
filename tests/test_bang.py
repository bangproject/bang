"""Framework tests.

Test the App framework.
"""
import pytest
# from pytest.mock import create_autospec

from .conftest import FixtureAPI
from bang.middleware import Middleware


FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"


# helpers

def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)

    return asset


# tests

def test_basic_route_adding(app):
    @app.route("/basic")
    def home(req, resp):
        resp.text = "YOLO"


def test_duplicate_routes_throws_exception(app):
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
    assert client.get("http://testserver/hello/Beast").text == "Hello, Beast"


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


def test_class_based_handler_not_allowed(app, client):
    @app.route("/wookie")
    class PersonResource:
        def post(self, req, resp):
            resp.text = "post"

    # and undefined method raises
    with pytest.raises(AttributeError):
        client.get("http://testserver/wookie").text


def test_add_route(app, client):
    def do_handle(req, resp):
        resp.text = "Route add method"

    app.add_route("/chewbaca", do_handle)
    assert client.get("http://testserver/chewbaca").text == "Route add method"


def test_template(app, client):
    @app.route("/html")
    def html_handler(req, resp):
        resp.body = app.template("index.html",
                                 context={
                                     "title": "Some Title",
                                     "name": "Some Name"
                                 }).encode()

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text


def test_custom_exception_handler(app, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"

    app.add_exception_handler(on_exception)

    @app.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/")

    assert response.text == "AttributeErrorHappened"


def test_404_is_returned_for_nonexistent_static_file(client):
    assert client.get("http://testserver/static/main.css)").status_code == 404


def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)
    app = FixtureAPI(static_dir=str(static_dir))
    client = app.test_session()

    response = client.get(f"http://testserver/static/{FILE_DIR}/{FILE_NAME}")

    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


def test_middleware_methods_are_called(app, client):
    process_request_called = False
    process_response_called = False

    class CallMiddlewareMethods(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, resp):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(CallMiddlewareMethods)

    app.reset_routes()

    @app.route('/')
    def index(req, res):
        res.text = "YOLO"

    client.get('http://testserver/')

    assert process_request_called is True
    assert process_response_called is True

    
def test_disallow_unhandled_methods_for_function_handlers(app, client):
    @app.route("/home3", allowed_methods=["post"])
    def home(req, resp):
        resp.text = "hello"

    with pytest.raises(AttributeError):
        client.get("http://testserver/home3")

    assert client.post("http://testserver/home3").text == "hello"
