"""Helper functions and classes for the tests."""

from . import conman


class MockResponse:
    """Mocked response object from the requests library."""

    def __init__(self, json_data=None, status_code=200):
        self.json_data = {}

        if isinstance(json_data, str):
            try:
                self.json_data = getattr(conman, json_data)
            except AttributeError as e:
                raise AttributeError(
                    'Missing conman response {}'.format(json_data)
                ) from e
        elif json_data:
            self.json_data = json_data

        self.status_code = status_code
        self.headers = ''

    @property
    def ok(self):
        return self.status_code == 200

    def json(self):
        return self.json_data

    @property
    def content(self):
        return str(self.json_data)


def mocked_requests(response=None):
    """
    Returns a callable that returns a MockResponse.

    Call this instead of calling requests.[method].
    """

    def wrapped(*args, **kwargs):
        if response:
            return MockResponse(response)
        else:
            return MockResponse()

    return wrapped
