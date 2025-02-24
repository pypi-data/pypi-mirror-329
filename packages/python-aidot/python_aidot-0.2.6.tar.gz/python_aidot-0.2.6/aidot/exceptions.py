"""aidot Exceptions."""
class AidotError(Exception):
    """Aidot api exception."""

class InvalidURL(AidotError):
    """Invalid url exception."""

class HTTPError(AidotError):
    """Invalid host exception."""

class InvalidHost(AidotError):
    """Invalid host exception."""

class AidotAuthTokenExpired(AidotError):
    """Authentication failed because token is invalid or expired."""

class AidotAuthFailed(AidotError):
    """Authentication failed because MFA verification code is required."""

class AidotUserOrPassIncorrect(AidotError):
    """The password or email address is incorrect."""
    