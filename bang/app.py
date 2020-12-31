"""Demo App

An inital demo user of our web app.
"""

from webob import Request, Response

from .api import BangAPI

app = BangAPI()


@app.route("/home")
def home(request: Request, response: Response):
    response.text = "Hello from the HOME page."


@app.route("/about")
def about(request: Request, response: Response):
    response.text = "Hello from the ABOUT page."
