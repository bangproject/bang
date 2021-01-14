"""Response is one of two HTTP message types as described in RFC 7231.

The bang Response type should be natural to anyone familiar with HTTP.
"""
import json
from dataclasses import dataclass

from webob import Response as WOResponse

@dataclass
class Response:
    status_code: int = None
    reason_phrase: str = None
    json: str = None
    html: str = None
    text: str = None
    content_type: str = None
    body: bytes = b''

    def __call__(self, environ, start_response):
        self.set_body_and_content_type()
        response = WOResponse(
            body=self.body, content_type=self.content_type, status=self.status_code
        )
        return response(environ, start_response)

    def set_body_and_content_type(self):
        if self.json is not None:
            self.body = json.dumps(self.json).encode('UTF-8')
            self.content_type = "application/json"

        if self.html is not None:
            self.body = self.html.encode()
            self.content_type = "text/html"

        if self.text is not None:
            self.body = self.text
            self.content_type = "text/plain"
