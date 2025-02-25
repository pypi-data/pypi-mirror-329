"""Library for exceptions using the Portainer API."""


class PortainerException(Exception):
    """Base class for all client exceptions."""


class ApiException(PortainerException):
    """Raised during problems talking to the API."""


class ApiBadRequestException(PortainerException):
    """Raised due sending a Rest command resulting in a bad request."""


class ApiForbiddenException(PortainerException):
    """Raised due to permission errors talking to API."""


class ApiUnauthorizedException(PortainerException):
    """Raised occasionally, mustn't harm the connection."""


class NoDataAvailableException(PortainerException):
    """Raised due updating data, when no data is available."""


class TimeoutException(PortainerException):
    """Raised due connecting the websocket."""
