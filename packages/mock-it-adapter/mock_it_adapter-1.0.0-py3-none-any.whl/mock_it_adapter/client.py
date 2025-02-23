import requests

from .exceptions import UnauthorizedError, ApiError, BadRequestError
from .models import Mock, MatcherType, Matcher


class MockITClient:
    def __init__(self, base_url):
        self.base_url = base_url

        self.session = requests.Session()

    def _make_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, params=params, json=data)

        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400:
            raise BadRequestError(f"Error create new Mock: \n {response.status_code}, {response.text}")
        elif response.status_code == 401:
            raise UnauthorizedError("Unauthorized")
        else:
            raise ApiError(f"API request failed: {response.status_code}, {response.text}")

    def create_mock(self,
                    method: str,
                    endpoint: str,
                    matcher: Matcher = None,
                    response_body: str = None,
                    status: int = 200,
                    name: str = None) -> object:

        body_patterns = f"{matcher.key},{matcher.value}" if matcher else None
        mock_name = (
            name
            if name is not None
            else (
                f"{endpoint}_{matcher.value}"
                if matcher is not None
                else f"{endpoint}"
            )
        )
        matcher_type = matcher.matcher_type if matcher else MatcherType.NONE
        mock: Mock = Mock(
            name=mock_name,
            url=endpoint,
            method=method,
            status_code=status,
            body=response_body,
            body_patterns=body_patterns,
            matcher_type=matcher_type
        )
        data = mock.model_dump()
        response = self._make_request("POST", "mocks", data=data)
        return f"New mock created: {response}"
