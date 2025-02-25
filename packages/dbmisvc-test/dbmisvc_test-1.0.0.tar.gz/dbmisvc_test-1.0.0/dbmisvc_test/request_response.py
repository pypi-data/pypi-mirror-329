from enum import StrEnum
from typing import Callable, Any, List

from django.test import Client
import responses


class Method(StrEnum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class RequestResponse:
    """
    This class creates instances of request/response interactions that
    are to be used in tests.
    """

    def __init__(
        self,
        name: str,
        mocks: List[responses.Response],
        client: Client,
        method: Method,
        url: str,
        data: dict[str, Any],
        status_code: int,
        content_type: str,
        assert_all_mocks_called: bool = True,
        successful: bool = False,
        handler: Callable = None,
    ):
        """
        :param name: The name of the subtest
        :type name: str
        :param mocks: A list of mocked responses to use for the test
        :type mocks: List[responses.Response]
        :param client: The client object to use as the caller
        :type client: Client
        :param method: The method of the request
        :type method: Method
        :param url: The URL for the request
        :type url: str
        :param data: A dictionary of arguments for the query or data of the request, depending on method, if any
        :type data: dict[str: Any]
        :param status_code: The expected status code of the response
        :type status_code: int
        :type content_type: The expected content type of the response
        :type content_type: str
        :param assert_all_mocks_called: Whether to require all passed mock responses to be called or not,
        defaults to True
        :type assert_all_mocks_called: bool
        :param successful: Whether this request/response definition describes a successful request or not,
        defaults to False
        :type successful: bool
        :param handler: A callable that is called after the request and passed the resultant response
        :type handler: Callable
        """
        self.name = name
        self.mocks = mocks
        self.client = client
        self.method = method
        self.url = url
        self.data = data
        self.status_code = status_code
        self.content_type = content_type
        self.assert_all_mocks_called = assert_all_mocks_called
        self.successful = successful
        self.handler = handler

    def call(self, assert_all_mocks_called: bool = True) -> responses.Response:
        """
        Calls the request/response interaction and returns the response.

        :param assert_all_mocks_called: Whether to require all passed mock responses to be called or not,
        defaults to True
        :type assert_all_mocks_called: bool
        :return: The response object
        :rtype: responses.Response
        """
        with responses.RequestsMock(
            assert_all_requests_are_fired=self.assert_all_mocks_called and assert_all_mocks_called
        ) as rsps:
            # Add all mocks to the context manager
            for mock in self.mocks:
                rsps.add(mock)

            # Make the request
            response = getattr(self.client, self.method.value)(self.url, self.data)

            # Check for handler to be called here
            if self.handler:
                self.handler(response)

            return response

    def get_response_mock(self, method: Method, url_substring: str = None):
        """
        Fetches and returns a mock response object based on the method and an optional URL substring.

        :param method: The HTTP method of the mock response to fetch
        :type method: Method
        :param url_substring: An optional substring to match against the mock response URL
        :type url_substring: str, optional
        :return: The matched mock response object
        :rtype: responses.Response
        """
        for mock in self.mocks:
            if mock.method.lower() == method.value.lower() and (
                url_substring is None or url_substring in str(mock.url)
            ):
                return mock
        return None
