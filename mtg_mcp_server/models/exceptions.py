"""Custom exception classes for MTG MCP Server."""


class MTGAPIError(Exception):
    """Base exception for MTG API related errors."""

    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class MTGAPIConnectionError(MTGAPIError):
    """Exception raised when unable to connect to MTG API."""

    def __init__(self, message: str = "Unable to connect to MTG API"):
        super().__init__(message)


class MTGAPITimeoutError(MTGAPIError):
    """Exception raised when MTG API request times out."""

    def __init__(self, message: str = "MTG API request timed out"):
        super().__init__(message)


class MTGAPIRateLimitError(MTGAPIError):
    """Exception raised when MTG API rate limit is exceeded."""

    def __init__(self, message: str = "MTG API rate limit exceeded"):
        super().__init__(message, status_code=429)


class MTGAPINotFoundError(MTGAPIError):
    """Exception raised when requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class MTGAPIServerError(MTGAPIError):
    """Exception raised when MTG API returns a server error."""

    def __init__(self, message: str = "MTG API server error", status_code: int = 500):
        super().__init__(message, status_code)


class MTGValidationError(Exception):
    """Exception raised for invalid input parameters."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
