"""BangAPI

This is the core for Bang web apps.
"""
import inspect
import os
from typing import Callable, Dict

from jinja2 import Environment, FileSystemLoader
from parse import parse
from webob import Request, Response

Handler = Callable[[Request], Response]


class BangAPI:
    """BangAPI is the WSGI compatible class for handling web requests.

    """
    routes: Dict[str, Handler] = {}
    templates_env: Environment = Environment(
        loader=FileSystemLoader(os.path.abspath("bang/templates")))
    exception_handler = None

    def __init__(self, templates_dir: str = None):
        if templates_dir is not None:
            self.templates_env = Environment(
                loader=FileSystemLoader(os.path.abspath(templates_dir)))

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path: str, handler: Handler):
        if path in self.routes:
            raise AttributeError(f"Route for path {path} already exists.")
        self.routes[path] = handler

    def route(self, path: str):
        def wrapper(handler: Handler):
            self.add_route(path, handler)
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

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method not allowed", request.method)
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler is None:
                print("self.exception_handler is None")
                raise e
            else:
                self.exception_handler(request, response, e)

        return response

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler
