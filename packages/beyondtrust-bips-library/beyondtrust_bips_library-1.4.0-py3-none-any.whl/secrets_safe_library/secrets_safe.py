"""SecretsSafe Module, all the logic to retrieve secrets from PS API"""

import logging
from urllib.parse import urlencode

import requests
from cerberus import Validator

from secrets_safe_library import exceptions, secrets, utils
from secrets_safe_library.authentication import Authentication


class SecretsSafe(secrets.Secrets):

    _authentication: Authentication = None
    _logger: logging.Logger = None
    _separator: str = None

    def __init__(self, authentication, logger=None, separator="/"):
        self._authentication = authentication
        self._logger = logger

        if len(separator.strip()) != 1:
            raise exceptions.LookupError(f"Invalid separator: {separator}")
        self._separator = separator

        # Schema rules used for validations
        self._schema = {
            "path": {"type": "string", "maxlength": 1792},
            "title": {"type": "string", "maxlength": 256, "nullable": True},
            "path_depth": {"max": 7},
        }
        self._validator = Validator(self._schema)

    def get_secret(self, path):
        """
        Get secret by path
        Arguments:
            path
        Returns:
            Retrieved secret string
        """

        utils.print_log(
            self._logger,
            "Running get_secret method in SecretsSafe class",
            logging.DEBUG,
        )
        secrets_dict = self.secrets_by_path_flow([path])
        return secrets_dict[path]

    def get_secret_with_metadata(self, path):
        """
        Get secret by path with metadata
        Arguments:
            path
        Returns:
           Retrieved secret in dict format
        """

        utils.print_log(
            self._logger,
            "Running get_secret method in SecretsSafe class",
            logging.DEBUG,
        )
        secrets_dict = self.secrets_by_path_flow([path], get_metadata=True)
        return secrets_dict

    def get_secrets(self, paths):
        """
        Get secrets by paths
        Arguments:
            paths list
        Returns:
            Retrieved secret in dict format
        """

        utils.print_log(
            self._logger,
            "Running get_secrets method in SecretsSafe class",
            logging.INFO,
        )
        secrets_dict = self.secrets_by_path_flow(paths)
        return secrets_dict

    def get_secrets_with_metadata(self, paths):
        """
        Get secrets by paths with metadata
        Arguments:
            paths list
        Returns:
            Retrieved secret in dict format
        """

        utils.print_log(
            self._logger,
            "Running get_secrets method in SecretsSafe class",
            logging.INFO,
        )
        secrets_dict = self.secrets_by_path_flow(paths, get_metadata=True)
        return secrets_dict

    def get_all_secrets_by_folder_path(self, folder_path):
        """
        Get all secrets by folder path
        Arguments:
            folder path
        Returns:
            Response (Dict)
        """

        response = {}
        secret_response = self.get_secret_by_path(
            folder_path, None, self._separator, send_title=False
        )
        for secret in secret_response.json():
            secret_path = f"{secret['FolderPath']}/{secret['Title']}"
            response[f"{secret_path}-metadata"] = secret
            if secret["SecretType"] == "File":
                response[secret_path] = self.get_file_secret_data(secret["Id"])
            else:
                response[secret_path] = secret["Password"]
        return response

    def get_file_secret_data(self, secret_id) -> str:
        """
        Gets secret file as an attachment based on secretId.

        Args:
            secret_id (str): The secret id (GUID).

        Returns:
            file secret content (str).
        """

        utils.print_log(self._logger, "Getting secret by file", logging.DEBUG)
        file_response = self._get_file_by_id_req(secret_id)

        if file_response.status_code != 200:
            if not self._authentication.sign_app_out():
                utils.print_log(self._logger, "Error in sign_app_out", logging.ERROR)
            raise exceptions.LookupError(
                f"Error getting file by id, message: {file_response.text}, statuscode: "
                f"{file_response.status_code}"
            )

        return file_response.text

    def secrets_by_path_flow(self, paths, get_metadata=False):
        """
        Secrets by path flow
        Arguments:
            paths list
        Returns:
            Response (Dict)
        """

        response = {}
        for path in paths:

            if not path:
                continue

            utils.print_log(
                self._logger,
                f"**************** secret path: {path} *****************",
                logging.INFO,
            )

            data = path.split(self._separator)

            if len(data) < 2:
                raise exceptions.LookupError(
                    f"Invalid secret path: {path}, check your path and title separator,"
                    f" separator must be: {self._separator}"
                )

            folder_path = data[:-1]
            title = data[-1]

            secret_response = self.get_secret_by_path(
                self._separator.join(folder_path), title, self._separator
            )

            if secret_response.status_code != 200:
                if not self._authentication.sign_app_out():
                    utils.print_log(
                        self._logger, "Error in sign_app_out", logging.ERROR
                    )
                raise exceptions.LookupError(
                    f"Error getting secret by path, message: {secret_response.text}, "
                    f"statuscode: {secret_response.status_code}"
                )

            secret = secret_response.json()
            if secret:
                utils.print_log(
                    self._logger,
                    f"Secret type: {secret[0]['SecretType']}",
                    logging.DEBUG,
                )

                if get_metadata:
                    response[f"{path}-metadata"] = secret[0]

                if secret[0]["SecretType"] == "File":
                    response[path] = self.get_file_secret_data(secret[0]["Id"])
                else:
                    response[path] = secret[0]["Password"]

                utils.print_log(
                    self._logger, "Secret was successfully retrieved", logging.INFO
                )
            else:
                raise exceptions.LookupError(f"{path}, Secret was not found")

        return response

    def get_secret_by_path(
        self, path: str, title: str, separator: str, send_title: bool = True
    ) -> requests.Response:
        """
        Get secrets by path and title.
        Arguments:
            path (str): The path where the secret is stored.
            title (str): The title used to identify the secret.
            separator (str): The separator used in the secret storage format.
            send_title (bool, optional): Flag to determine if the title should be
                included in the request. Defaults to True.

        Returns:
            requests.Response: A response object containing the secret.

        Raises:
            exceptions.OptionsError: If any of the schema rules are not valid.
        """

        path_depth = path.count(separator) + 1
        attributes = {"path": path, "title": title, "path_depth": path_depth}

        if self._validator.validate(attributes, update=True):
            query_params = {"path": path, "separator": separator}

            if self._authentication._api_version:
                query_params["version"] = self._authentication._api_version

            if send_title:
                query_params["title"] = title

            params = urlencode(query_params)

            url = f"{self._authentication._api_url}/secrets-safe/secrets?{params}"

            utils.print_log(
                self._logger,
                f"Calling get_secret_by_path endpoint: {url}",
                logging.DEBUG,
            )
            response = self._run_get_request(url)
            return response
        else:
            raise exceptions.OptionsError(f"Please check: {self._validator.errors}")

    def _get_file_by_id_req(self, secret_id):
        """
        Get a File secret by File id
        Arguments:
            secret id
        Returns:
            File secret text
        """

        url = (
            f"{self._authentication._api_url}/secrets-safe/secrets/{secret_id}"
            "/file/download"
        )

        if self._authentication._api_version:
            url = f"{url}?version={self._authentication._api_version}"

        utils.print_log(
            self._logger, f"Calling _get_file_by_id_req endpoint: {url}", logging.DEBUG
        )
        response = self._run_get_request(url)
        return response

    def _run_get_request(self, url: str) -> requests.Response:
        """
        Shortcut function to make a GET request to the specified URL using
        Authentication object.

        Args:
            url (str): The URL to call using GET HTTP verb.

        Returns:
            request.Response: Response object.
        """
        if self._authentication._api_version:
            query_sep = "&" if url.find("?") else "?"
            url = f"{url}{query_sep}version={self._authentication._api_version}"

        response = self._authentication._req.get(
            url,
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )
        return response

    def get_secret_by_id(self, secret_id: str) -> dict:
        """
        Find a secret by ID.

        Args:
            secret_id (str): The secret ID (GUID).

        Returns:
            dict: Secret object according requested API version.

        Raises:
            exceptions.LookupError: Raised when no secret is found using secret_id.
        """

        url = f"{self._authentication._api_url}/secrets-safe/secrets/{secret_id}"

        utils.print_log(
            self._logger, f"Calling get_secret_by_id endpoint: {url}", logging.DEBUG
        )
        response = self._run_get_request(url)

        if response.status_code != 200:
            if not self._authentication.sign_app_out():
                utils.print_log(
                    self._logger, "Error in get_secret_by_id", logging.ERROR
                )
            raise exceptions.LookupError(
                f"Error getting secret by id, message: {response.text}, statuscode: "
                f"{response.status_code}"
            )

        return response.json()

    def list_secrets(
        self,
        path: str = None,
        separator: str = None,
        title: str = None,
        afterdate: str = None,
        limit: int = None,
        offset: int = None,
    ) -> list:
        """
        Returns a list of secrets with the option to filter the list using query
        parameters.

        Args:
            path (str): the full path to the secret.
            separator (str): the separator used in the path above. Default is /.
            title (str): the full title of the secret.
            afterdate (str): filter by modified or created on, after, or equal to the
            given date. Must be in the following UTC format: yyyy-MM-ddTHH:mm:ssZ.
            limit (int): limit the results.
            offset (int): skip the first (offset) number of secrets.

        Returns:
            list: List of secrets matching specified arguments.
        """

        params = {
            "path": path,
            "separator": separator,
            "title": title,
            "afterdate": afterdate,
            "limit": limit,
            "offset": offset,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        query_string = urlencode(query_params)
        url = f"{self._authentication._api_url}/secrets-safe/secrets?{query_string}"

        utils.print_log(
            self._logger, f"Calling list_secrets endpoint: {url}", logging.DEBUG
        )
        response = self._run_get_request(url)

        if response.status_code != 200:
            if not self._authentication.sign_app_out():
                utils.print_log(self._logger, "Error in list_secrets", logging.ERROR)
            raise exceptions.LookupError(
                f"Error getting secrets, message: {response.text}, statuscode: "
                f"{response.status_code}"
            )

        return response.json()
