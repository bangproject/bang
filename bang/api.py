"""BangAPI

This is the core for Bang web apps.
"""

from typing import Dict, Callable, NewType

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

    def handle_request(self, request: Request) -> Response:
        response = Response()
        print(self.routes)
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response
