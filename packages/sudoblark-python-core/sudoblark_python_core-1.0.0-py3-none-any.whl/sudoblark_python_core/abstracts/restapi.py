"""
This module is responsible for defining base abstract classes for interacting with RESTful APIs.
"""

import logging
import os

# Native modules
from abc import ABC, abstractmethod
from typing import Union

# Third party modules
import requests

# Constants required for our classes etc
LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class IClient(ABC):
    """
    Interface definition for a RESTAPI client
    """

    @abstractmethod
    def _get_auth_secret_environment_variable(self) -> str:
        """
        Raises:
            NotImplementedError: If child class has not implemented method

        Returns:
            Name of the environment variable we will use to get the auth secret.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_auth_type(self) -> str:
        """
        Raises:
            NotImplementedError: If child class has not implemented method

        Returns:
            Type of authentication we wish to use for connecting to the RESTAPI.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_base_url(self) -> str:
        """
        Raises:
            NotImplementedError: If child class has not implemented method

        Returns:
            Base URL we should use for querying this RESTAPI.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_auth_endpoint(self) -> str:
        """
        Raises:
            NotImplementedError: If child class has not implemented method

        Returns:
            Endpoint on the RESTAPI we'll use to confirm instance can authentication.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_api_name(self) -> str:
        """
        Raises:
            NotImplementedError: If child class has not implemented method

        Returns:
            Name of the API we're connecting to.
        """
        raise NotImplementedError

    # Python can't do overloading, so we instead have one big constructor
    def __init__(self, auth_secret: Union[None, str] = None):
        """
        Args:
            auth_secret (str): The secret used to authenticate with the RESTAPI, if None will attempt
                                read from _get_auth_secret_environment_variable() instead.

        Raises:
            requests.ConnectionError: If unable to connect to the RESTAPI via _get_auth_endpoint
        """
        try:
            self.headers: dict = self.return_supported_auth()[self._get_auth_type().lower()](auth_secret)
        except KeyError:
            LOGGER.error(
                "The selected auth type %s is currently not supported. The supported auth types are: %s",
                self._get_auth_type(),
                ",".join(self.return_supported_auth().keys()),
            )

        if self.test_authentication():
            self.client: requests.Session = requests.Session()
            self.client.headers.update(self.headers)
            self.__post__init()
        else:
            raise requests.ConnectionError

    def __post__init(self):
        """
        Method provided to allow for extra behaviour in constructor once IClient finishes
        """
        pass

    def return_supported_auth(self) -> dict:
        """
        Returns:
            Dictionary of supported auth types to methods for generating their headers for self.client
        """

        return {"bearer": self.return_header_authorization}

    def return_header_authorization(self, auth_secret: Union[None, str]) -> dict:
        """
        Returns authorization headers
        Args:
            auth_secret: The secret used to authenticate with the RESTAPI, if None will attempt
                                read from _get_auth_secret_environment_variable() instead.

        Returns:
            Headers to use for `self.client`
        """
        return {
            "Authorization": f"{self._get_auth_type()} " + self._get_token(auth_secret, self._get_auth_secret_environment_variable()),
            "Accept": "application/json",
        }

    def test_authentication(self) -> bool:
        """
        Returns:
            bool: True if we can authenticate with the RESTAPI, False otherwise.
        """
        connected: bool = False
        auth_request: requests.Response = requests.get(
            url=f"{self._get_base_url()}{self._get_auth_endpoint()}", headers=self.headers, timeout=10
        )

        if auth_request.status_code == 200:
            # Lazy logging so we interpolate only if message is actually omitted
            LOGGER.debug("Successfully connected to %s and queried %s endpoint", self._get_api_name(), self._get_auth_endpoint())
            connected = True
        else:
            LOGGER.error("Unable to connect to %s via %s endpoint, see exact error below.", self._get_api_name(), self._get_auth_endpoint())
            LOGGER.error("%s", auth_request.content.decode("utf-8").replace("\r\n", ". "))

        return connected

    @staticmethod
    def _get_token(auth_secret: Union[None, str], environment_variable: str) -> str:
        """
        Private method to determine token to utilise for auth header.

        Args:
            auth_secret: String if token passed explicitly, else None to indicate attempted
                        lookup via environment variable
            environment_variable: Name of the environment variable to lookup token from
                                  if auth_secret is None

        Raises:
            ValueError: If unable to determine token from auth_secret or environment_variable.


        Returns:
            The token to utilise for `self.client` authorisation header
        """
        return_secret: Union[None, str] = auth_secret

        if auth_secret is None:
            LOGGER.debug("No token provided, attempting to read from %s", environment_variable)

            if environment_variable in os.environ:
                return_secret = os.getenv(environment_variable)
            else:
                LOGGER.error("%s environment variable not set and no TOKEN passed through", environment_variable)
                raise ValueError("%s environment variable not set and no TOKEN passed through", environment_variable)

        return return_secret

    def __str__(self) -> str:
        """
        Returns:
            Information string representation
        """
        return f"{self._get_auth_type()}:{self._get_api_name()}@{self._get_base_url()}"

    def __hash__(self) -> int:
        """
        Returns:
            Unique int representation of instance.
        """
        return hash((self._get_auth_type(), self._get_api_name(), self._get_base_url()))

    def __eq__(self, other: object) -> bool:
        """
        Args:
            other: Object to compare against

        Returns:
            True if instances are equal, False otherwise.
        """
        if not isinstance(other, type(self)):
            return False
        return (
            self._get_auth_type() == other._get_auth_type()
            and self._get_api_name() == other._get_api_name()
            and self._get_base_url() == other._get_base_url()
        )
