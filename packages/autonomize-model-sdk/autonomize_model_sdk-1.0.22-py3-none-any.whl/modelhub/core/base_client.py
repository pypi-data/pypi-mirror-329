""" This module contains the BaseClient class for handling common HTTP operations and token management. """

import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..utils import setup_logger
from .exceptions import ModelHubException
from .response import handle_response

load_dotenv()
logger = setup_logger(__name__)


class BaseClient:
    """Base client for handling common HTTP operations and token management."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 10,
    ):
        """
        Initialize a new instance of the BaseClient class.

        Args:
            base_url (str, optional): The base URL of the API. Defaults to None.
            client_id (str, optional): The client ID for authentication. Defaults to None.
            client_secret (str, optional): The client secret for authentication. Defaults to None.
            token (str, optional): The access token for authentication. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 10.

        Raises:
            ModelHubException: If base URL is not provided or empty.
        """
        # Initialize base URL
        base_url = base_url or os.getenv("MODELHUB_BASE_URL", "").strip()
        if not base_url:
            logger.error("Base URL not provided")
            raise ModelHubException("Base URL is required")
        self.base_url = base_url
        self.client_id = client_id or os.getenv("MODELHUB_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("MODELHUB_CLIENT_SECRET")
        self.token = token or os.getenv("MODELHUB_TOKEN")
        self.timeout = timeout
        self.headers: Dict[str, str] = {}
        self.session = self._setup_session()

        logger.debug("Initializing client with base URL: %s", self.base_url)

        # Set up authentication
        if self.token and self.token.strip():
            logger.debug("Using provided token for authentication")
            self.headers = {"Authorization": f"{self.token}"}
        elif (
            self.client_id
            and self.client_secret
            and self.client_id.strip()
            and self.client_secret.strip()
        ):
            logger.debug("Getting token using client credentials")
            self.get_token()

    @property
    def modelhub_url(self) -> str:
        """Compute the ModelHub API URL based on the base URL."""
        return f"{self.base_url}/modelhub/api/v1"

    @property
    def auth_url(self) -> str:
        """Compute the Authentication API URL based on the base URL."""
        return f"{self.base_url}/ums/api/v1"

    def _setup_session(self) -> requests.Session:
        """
        Set up a requests session with retry configuration.

        Returns:
            requests.Session: Configured session object.
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_token(self) -> None:
        """
        Fetch a token using the client credentials flow and store it.

        Raises:
            ModelHubException: If token is not found in response data.
        """
        token_endpoint = f"{self.auth_url}/auth/get-token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        logger.debug("Requesting new auth token")
        try:
            response = self.session.post(
                token_endpoint, json=payload, timeout=self.timeout
            )
            response_data = handle_response(response)

            if "token" not in response_data:
                logger.error("Token not found in response data")
                raise ModelHubException("Token not found in response data")

            self.token = response_data["token"]["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            logger.debug("Successfully obtained new auth token")

        except requests.exceptions.RequestException as e:
            logger.error("Failed to get auth token: %s", str(e))
            raise

    def request_with_retry(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Send a request and retry with a new token if unauthorized.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The endpoint to send the request to.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            dict: The response data.

        Raises:
            ModelHubException: If request fails after retry.
        """
        url = f"{self.modelhub_url}/{endpoint}"
        logger.debug("Making %s request to: %s", method, url)

        try:
            kwargs.setdefault("timeout", self.timeout)
            response = self.session.request(method, url, headers=self.headers, **kwargs)

            # Handle 401 by refreshing token and retrying
            if response.status_code == 401 and self.client_id and self.client_secret:
                logger.debug("Received 401, refreshing token and retrying")
                self.get_token()
                kwargs["headers"] = self.headers
                response = self.session.request(method, url, **kwargs)

            return handle_response(response)

        except requests.exceptions.RequestException as e:
            logger.error("Request failed: %s", str(e))
            raise

    def post(
        self,
        endpoint: str,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
        files: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Send a POST request to the specified endpoint."""
        return self.request_with_retry(
            "post", endpoint, json=json, params=params, files=files, data=data
        )

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Send a GET request to the specified endpoint."""
        return self.request_with_retry("get", endpoint, params=params)

    def put(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Send a PUT request to the specified endpoint."""
        return self.request_with_retry("put", endpoint, json=json)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Send a DELETE request to the specified endpoint."""
        return self.request_with_retry("delete", endpoint)
