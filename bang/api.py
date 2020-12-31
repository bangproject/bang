"""BangAPI

This is the core for Bang web apps.
"""

from typing import Dict, Callable, NewType

from parse import parse
from webob import Request, Response


Handler = NewType('Handler', Callable[[Request], Response])


class BangAPI:
    """BangAPI is the WSGI compatible class for handling web requests.

    """
    routes: Dict[str, Handler] = {}


    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)


    def route(self, path: str):
        def wrapper(handler: Handler):
            self.routes[path] = handler
            return handler

        return wrapper


    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."


    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None


    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response


    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."
