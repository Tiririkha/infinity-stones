class TimestoneError(Exception):
    """Base exception for Timestone errors"""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

    def __str__(self):
        if self.status_code:
            return f"Error (Status Code {self.status_code}): {self.message}"
        return f"{self.message}"


class TimestoneAuthError(TimestoneError):
    """Raised when authentication fails"""
    pass


class TimestoneBadRequestError(TimestoneError):
    """Raised when the request is malformed."""
    pass


class TimestoneForbiddenError(TimestoneError):
    """Raised when the client does not have permission to access the resource."""
    pass


class TimestoneNotFoundError(TimestoneError):
    """Raised when the requested resource is not found."""
    pass


class TimestoneMethodNotAllowedError(TimestoneError):
    """Raised when the requested method is not supported by the resource."""
    pass


class TimestoneNotAcceptableError(TimestoneError):
    """Raised when the server cannot produce a response that the client accepts."""
    pass


class TimestoneRequestTimeoutError(TimestoneError):
    """Raised when the server did not receive a timely response from the client."""
    pass


class TimestoneConflictError(TimestoneError):
    """Raised when the request could not be completed due to a conflict with the current state of the resource."""
    pass


class TimestoneGoneError(TimestoneError):
    """Raised when the resource is no longer available and will not be available again."""
    pass


class TimestoneLengthRequiredError(TimestoneError):
    """Raised when the request did not include a required Content-Length header."""
    pass


class TimestonePreconditionFailedError(TimestoneError):
    """Raised when the server does not meet one of the preconditions that the requester put on the request."""
    pass


class TimestonePayloadTooLargeError(TimestoneError):
    """Raised when the request entity is larger than the server is willing or able to process."""
    pass


class TimestoneURITooLongError(TimestoneError):
    """Raised when the length of the requested URI exceeds the server's capacity to handle."""
    pass


class TimestoneUnsupportedMediaTypeError(TimestoneError):
    """Raised when the server cannot process the entity of the request due to the media type."""
    pass


class TimestoneRangeNotSatisfiableError(TimestoneError):
    """Raised when the requested range of resource is not satisfiable."""
    pass


class TimestoneExpectationFailedError(TimestoneError):
    """Raised when a precondition given in the Expect request-header fields could not be met by the server."""
    pass


class TimestoneValidationError(TimestoneError):
    """Raised when validation fails."""
    pass


class TimestoneRateLimitError(TimestoneError):
    """Raised when rate limit is exceeded."""
    pass


class TimestoneRequestHeaderFieldsTooLargeError(TimestoneError):
    """Raised when the size of the request headers exceeds the server's capacity."""
    pass


class TimestoneUnavailableForLegalReasonsError(TimestoneError):
    """Raised when the server is refusing to service the request because the user has violated the use policies for that service."""
    pass


class TimestoneAPIError(TimestoneError):
    """Raised when API returns an error."""
    pass


class TimestoneConnectionError(TimestoneError):
    """Raised when connection to API fails."""
    pass
