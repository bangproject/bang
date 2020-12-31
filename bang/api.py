
from webob import Request, Response

class BangAPI(object):
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request) 
        return response(environ, start_response)

    def handle_request(self, request: Request) -> Response:
        user_agent = request.environ.get("HTTP_USER_AGENT", "No user agent found.")

        response = Response()
        response.text = f"Your user-agent is {user_agent}."

        return response