"""Custom exceptions for the Agent Trust Stack hosted client."""


class AgentTrustError(Exception):
    """Base exception for all Agent Trust Stack API errors."""

    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(AgentTrustError):
    """Raised when authentication fails (401)."""
    pass


class AuthorizationError(AgentTrustError):
    """Raised when the agent lacks permission (403)."""
    pass


class NotFoundError(AgentTrustError):
    """Raised when a resource is not found (404)."""
    pass


class ValidationError(AgentTrustError):
    """Raised when request validation fails (400)."""
    pass


class RateLimitError(AgentTrustError):
    """Raised when rate limits are exceeded (429)."""

    def __init__(self, message, status_code=429, response_body=None, retry_after=None):
        super().__init__(message, status_code, response_body)
        self.retry_after = retry_after


class ConflictError(AgentTrustError):
    """Raised on resource conflicts (409)."""
    pass


class ServerError(AgentTrustError):
    """Raised on server-side errors (5xx)."""
    pass
