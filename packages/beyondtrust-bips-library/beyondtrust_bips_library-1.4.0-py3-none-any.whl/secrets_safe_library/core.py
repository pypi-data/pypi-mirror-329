import logging
from abc import ABC, abstractmethod
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

from secrets_safe_library import exceptions, utils
from secrets_safe_library.authentication import Authentication


class APIObjectInterface(ABC):
    @abstractmethod
    def _run_get_request(
        self, endpoint: str, include_api_version: bool, expected_status_code: int
    ) -> requests.Response:
        pass

    @abstractmethod
    def _run_post_request(
        self,
        endpoint: str,
        payload: dict,
        include_api_version: bool,
        expected_status_code: int,
    ) -> requests.Response:
        pass

    @abstractmethod
    def _run_delete_request(
        self, endpoint: str, expected_status_code: int
    ) -> requests.Response:
        pass

    @abstractmethod
    def make_query_string(self, params: dict) -> str:
        pass


class APIObject(APIObjectInterface):
    _authentication: Authentication
    _logger: logging.Logger

    def __init__(self, authentication: Authentication, logger: logging.Logger = None):
        self._authentication = authentication
        self._logger = logger

    def _run_get_request(
        self,
        endpoint: str,
        include_api_version: bool = True,
        expected_status_code: int = 200,
    ) -> requests.Response:
        """
        Shortcut function to make a GET request to the specified endpoint using
        Authentication object.

        Args:
            endpoint (str): The endpoint to call using GET HTTP verb.
            include_api_version (bool): Whether to include API version in request URL.
            expected_status_code (int, optional): Expected status code to consider the
                request was successful.

        Returns:
            request.Response: Response object.

        Raises:
            exceptions.LookupError: When get request fails.
        """
        url = self._create_url(endpoint, include_api_version)

        utils.print_log(self._logger, f"GET request to URL: {url}", logging.DEBUG)

        response = self._authentication._req.get(
            url,
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )

        if response.status_code != expected_status_code:
            if not self._authentication.sign_app_out():
                utils.print_log(
                    self._logger, "Error running get request", logging.ERROR
                )
            raise exceptions.LookupError(
                f"Error running get request, message: {response.text}, statuscode: "
                f"{response.status_code}"
            )

        return response

    def _run_post_request(
        self,
        endpoint: str,
        payload: dict,
        include_api_version: bool = True,
        expected_status_code: int = 201,
    ) -> requests.Response:
        """
        Shortcut function to make a POST request to the specified endpoint using
        Authentication object.

        Args:
            endpoint (str): The endpoint to call using POST HTTP verb.
            payload (dict): Payload to send with the POST request.
            include_api_version (bool): Whether to include API version in request URL.
            expected_status_code (int, optional): Expected status code to consider the
                request was successful.

        Returns:
            request.Response: Response object.

        Raises:
            exceptions.CreationError: Raised when folder was not created.
        """
        url = self._create_url(endpoint, include_api_version)

        utils.print_log(self._logger, f"Calling URL: {url}", logging.DEBUG)

        response = self._authentication._req.post(
            url=url,
            data=payload,
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )

        if response.status_code != expected_status_code:
            if not self._authentication.sign_app_out():
                utils.print_log(self._logger, "Error in post request", logging.ERROR)
            raise exceptions.CreationError(
                f"Error running post request, message: {response.text}, statuscode: "
                f"{response.status_code}"
            )

        return response

    def _run_delete_request(
        self,
        endpoint: str,
        expected_status_code: int = 200,
    ) -> None:
        """
        Shortcut function to make a DELETE request to the specified endpoint using
        Authentication object.

        Args:
            endpoint (str): The endpoint to call using DELETE HTTP verb.
            include_api_version (bool): Whether to include API version in request URL.
            expected_status_code (int, optional): Expected status code to consider the
                request was successful.

        Returns:
            request.Response: Response object.

        Raises:
            exceptions.DeletionError: When delete request fails.
        """
        url = self._create_url(endpoint, include_api_version=False)

        utils.print_log(self._logger, f"DELETE request to URL: {url}", logging.DEBUG)

        response = self._authentication._req.delete(
            url,
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )

        if response.status_code != expected_status_code:
            if not self._authentication.sign_app_out():
                utils.print_log(
                    self._logger, "Error running delete request", logging.ERROR
                )
            raise exceptions.DeletionError(
                f"Error running delete request, message: {response.text}, statuscode: "
                f"{response.status_code}"
            )

    def _create_url(self, endpoint: str, include_api_version: bool = True) -> str:
        """
        Constructs a complete URL by appending the specified endpoint to the base API
        URL.
        Optionally includes the API version as a query parameter.

        Args:
            endpoint (str): The endpoint to be appended to the base API URL. This should
                start with a '/'.
            include_api_version (bool): Flag to determine whether to include the API
                version in the URL. Defaults to True. If True and the API version is
                specified in the authentication object, it will be included as a query
                parameter.

        Returns:
            str: The fully constructed URL.

        Example:
            If the base API URL is "http://api.example.com", the endpoint is "/data",
            and the API version is "v1", then the resulting URL will be
            "http://api.example.com/data?version=v1" if  include_api_version is True.
            If include_api_version is False, the resulting URL will be
            "http://api.example.com/data".
        """
        url = f"{self._authentication._api_url}{endpoint}"

        if self._authentication._api_version and include_api_version:
            params = {"version": self._authentication._api_version}
            url = self.add_api_version(url=url, new_params=params)
        return url

    def add_api_version(self, url: str, new_params: dict) -> str:
        """
        Appends or updates query parameters in the given URL.

        This function parses the provided URL, updates its query parameters with the new
        parameters provided, and reconstructs the URL.

        Args:
            url (str): The original URL to which parameters will be added or updated.
            new_params (dict): A dictionary of parameters to add or update in the URL.
                The dictionary should have parameter names as keys and parameter values
                as values.

        Returns:
            str: The new URL with updated query parameters.

        Example:
            Given the URL "http://example.com/data?filter=old" and new_params
            {"version": "v1", "filter": "new"}, the function returns
            "http://example.com/data?filter=new&version=v1".
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params.update(new_params)

        query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=query))
        return new_url

    def make_query_string(self, params: dict) -> str:
        """
        Constructs a query string from a dictionary of parameters, excluding any
        parameters with a value of None.

        This function filters out any key-value pairs in the input dictionary where the
        value is None, and then encodes the remaining parameters into a URL-encoded
        query string.

        Args:
            params (dict): A dictionary containing the parameters to be included in the
                query string. Keys are parameter names, and values are parameter values.
                Parameters with None values are excluded from the resulting query
                string.

        Returns:
            str: A URL-encoded query string constructed from the provided parameters. If
                all parameters are None, returns an empty string.

        Example:
            Given params = {"name": "John", "age": 30, "city": None}, the function
            returns "name=John&age=30".
        """
        query_params = {k: v for k, v in params.items() if v is not None}
        query_string = urlencode(query_params)
        return query_string
