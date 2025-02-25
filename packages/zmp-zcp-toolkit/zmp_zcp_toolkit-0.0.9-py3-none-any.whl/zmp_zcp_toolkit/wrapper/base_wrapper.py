import logging
import os
from abc import abstractmethod
from enum import Enum
from typing import Any, Dict

from httpx import AsyncClient, BasicAuth, Client, Response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_TIMEOUT = os.getenv("HTTPX_DEFAULT_TIMEOUT", 10)


class AuthenticationType(str, Enum):
    """Authentication type model"""

    NONE = "None"
    BASIC = "Basic"
    BEARER = "Bearer"


class BaseAPIWrapper:
    def __init__(
        self,
        server: str,
        /,
        *,
        headers: dict | None = None,
        cookies: dict | None = None,
        auth_type: AuthenticationType | None = AuthenticationType.NONE,
        username: str | None = None,
        password: str | None = None,
        bearer_token: str | None = None,
        tls_verify: bool | None = False,
        timeout: int | None = _TIMEOUT,
    ):
        if not server:
            raise ValueError("Server URL is required")

        self._server = server
        self._headers = headers if headers is not None else {}
        self._cookies = cookies if cookies is not None else {}
        self._auth_type = auth_type
        self._username = username
        self._password = password
        self._bearer_token = bearer_token
        self._tls_verify = tls_verify
        self._timeout = timeout
        self._auth = None
        self._client = None
        self._async_client = None

        if auth_type == AuthenticationType.BASIC:
            if not username or not password:
                raise ValueError(
                    "Username and password are required for Basic authentication"
                )
            self._auth = BasicAuth(username=username, password=password)
        elif auth_type == AuthenticationType.BEARER:
            if not bearer_token:
                raise ValueError("Bearer token is required for Bearer authentication")

        if self._headers.get("Content-Type") is None:
            self._headers.update({"Content-Type": "application/json"})

        if (
            self._auth_type == AuthenticationType.BEARER
            and self._bearer_token is not None
        ):
            self._headers.update({"Authorization": f"Bearer {self._bearer_token}"})


    @property
    def server(self) -> str:
        """Get the server URL."""
        return self._server

    @property
    def async_client(self) -> AsyncClient:
        if self._async_client is None:
            self._async_client = AsyncClient(
                auth=self._auth,
                base_url=self._server,
                headers=self._headers,
                cookies=self._cookies,
                verify=self._tls_verify,
                timeout=self._timeout,
            )
        return self._async_client

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(
                auth=self._auth,
                base_url=self._server,
                headers=self._headers,
                cookies=self._cookies,
                verify=self._tls_verify,
                timeout=self._timeout,
            )
        return self._client

    async def get_response(self, response: Response) -> Dict[str, Any]:
        """Get response from API.

        Args:
            response (Response): Response from API

        Returns:
            Dict[str, Any]: Response data
        """
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(
                f"Failed to get response: {response.status_code} {response.text}"
            )
            return {
                "result": "failed",
                "code": response.status_code,
                "message": response.text,
            }

    async def close(self) -> None:
        """Close the async client."""
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    @abstractmethod
    def run(self, mode: str, query: Any) -> str:
        """Run the API wrapper with the given mode and query.

        Args:
            mode (str): Operation mode
            query (Any): Query parameters

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Returns:
            str: Response from API
        """
        ...
