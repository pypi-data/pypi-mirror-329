"""Module for AbstractAuth for aiotainer."""

import logging
from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

from aiohttp import (
    ClientError,
    ClientResponse,
    ClientResponseError,
    ClientSession,
)

from .exceptions import (
    ApiBadRequestException,
    ApiException,
    ApiForbiddenException,
    ApiUnauthorizedException,
)

ERROR = "error"
STATUS = "status"
MESSAGE = "message"

_LOGGER = logging.getLogger(__name__)


class Auth:
    """Class to make authenticated requests."""

    def __init__(
        self, websession: ClientSession, host_url: str, access_token: str
    ) -> None:
        """Initialize the auth."""
        self._websession = websession
        self.host_url = host_url
        self.access_token = access_token

    async def request(self, method: str, url: str, **kwargs: Any) -> ClientResponse:
        """Make a request."""
        access_token = self.access_token
        headers = {
            "X-Api-Key": access_token,
        }
        if not url.startswith(("http://", "https://")):
            host_url = self.host_url
            if not host_url.startswith(("http://", "https://")):
                host_url = f"https://{self.host_url}"
            url = f"{host_url}/{url}"
        _LOGGER.debug("request[%s]=%s %s", method, url, kwargs.get("params"))
        if method != "get" and "json" in kwargs:
            _LOGGER.debug("request[post json]=%s", kwargs["json"])
        return await self._websession.request(
            method, url, ssl=False, **kwargs, headers=headers
        )

    async def get(self, url: str, **kwargs: Any) -> ClientResponse:
        """Make a get request."""
        _LOGGER.debug("url: %s", url)
        try:
            resp = await self.request("get", url, **kwargs)
        except ClientError as err:
            raise ApiException(f"Error connecting to API: {err}") from err
        return await Auth._raise_for_status(resp)

    async def get_json(self, url: str, **kwargs: Any) -> Any:
        """Make a get request and return json response."""
        resp = await self.get(url, **kwargs)
        try:
            result = await resp.json(encoding="UTF-8")
        except ClientError as err:
            raise ApiException("Server returned malformed response") from err
        if not isinstance(result, list | dict):
            raise ApiException(f"Server return malformed response: {result}")
        _LOGGER.debug("response=%s", result)
        return result

    async def get_json_node(self, url: str, **kwargs: Any) -> Mapping[Any, Any]:
        """Make a get request and return json response."""
        resp = await self.get(url, **kwargs)
        try:
            result = await resp.json(encoding="UTF-8")
        except ClientError as err:
            raise ApiException("Server returned malformed response") from err
        if not isinstance(result, dict):
            raise ApiException(f"Server return malformed response: {result}")
        _LOGGER.debug("response=%s", result)
        return result

    async def post(self, url: str, **kwargs: Any) -> ClientResponse:
        """Make a post request."""
        try:
            resp = await self.request("post", url, **kwargs)
        except ClientError as err:
            raise ApiException(f"Error connecting to API: {err}") from err
        return await Auth._raise_for_status(resp)

    async def post_json(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """Make a post request and return a json response."""
        resp = await self.post(url, **kwargs)
        try:
            result = await resp.json()
        except ClientError as err:
            raise ApiException("Server returned malformed response") from err
        if not isinstance(result, dict):
            raise ApiException(f"Server returned malformed response: {result}")
        _LOGGER.debug("response=%s", result)
        return result

    @staticmethod
    async def _raise_for_status(resp: ClientResponse) -> ClientResponse:
        """Raise exceptions on failure methods."""
        detail = await Auth._error_detail(resp)
        try:
            resp.raise_for_status()
        except ClientResponseError as err:
            if err.status == HTTPStatus.BAD_REQUEST:
                raise ApiBadRequestException(
                    f"Unable to send request with API: {err}"
                ) from err
            if err.status == HTTPStatus.UNAUTHORIZED:
                raise ApiUnauthorizedException(
                    f"Unable to authenticate with API: {err}"
                ) from err
            if err.status == HTTPStatus.FORBIDDEN:
                raise ApiForbiddenException(
                    f"Forbidden response from API: {err}"
                ) from err
            detail.append(err.message)
            raise ApiException(": ".join(detail)) from err
        except ClientError as err:
            raise ApiException(f"Error from API: {err}") from err
        return resp

    @staticmethod
    async def _error_detail(resp: ClientResponse) -> list[str]:
        """Return an error message string from the API response."""
        if resp.status < 400:
            return []
        try:
            result = await resp.json()
            error = result.get(ERROR, {})
        except ClientError:
            return []
        message = ["Error from API", f"{resp.status}"]
        if STATUS in error:
            message.append(f"{error[STATUS]}")
        if MESSAGE in error:
            message.append(error[MESSAGE])
        return message
