"""Demo App

An inital demo user of our web app.
"""

from webob import Request, Response

from bang.api import BangAPI
from bang.middleware import Middleware

app = BangAPI()


@app.route("/home")
def home(request: Request, response: Response):
    response.text = "Hello from the HOME page."


@app.route("/about")
def about(request: Request, response: Response):
    response.text = "Hello from the ABOUT page."


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    def put(self, req, resp):
        resp.text = "Endpoint to overwrite/create a book"

    def delete(self, req, resp):
        resp.text = "Endpoint to delete a book"


def custom_exception_handler(request, response, exception_cls):
    response.text = str(exception_cls)


app.add_exception_handler(custom_exception_handler)


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)


@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template("index.html",
                             context={
                                 "name": "bang",
                                 "title": "Bangin' Framework"
                             })


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}


@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"
