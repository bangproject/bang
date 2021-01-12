"""conftest

Defines fixtures in a conventional filename for automatic discovery and instantiation by pytest
during the test collection phase.
"""
import pytest
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from bang.api import BangAPI


class FixtureAPI(BangAPI):
    def __init__(self, static_dir="static"):
        super().__init__(static_dir=static_dir)

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session


@pytest.fixture
def app():
    """A version of the API that includes a test_session method."""
    return FixtureAPI()


@pytest.fixture
def client(app):
    return app.test_session()
