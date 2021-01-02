"""Demo App

An inital demo user of our web app.
"""

from webob import Request, Response

from bang.api import BangAPI

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
