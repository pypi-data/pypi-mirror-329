from typing import Literal

__all__ = [
    "SauceNaoError",
    "SauceNaoServerError",
    "InvalidApiKeyError",
    "RateLimitedError",
    "UploadError",
    "FileSizeError",
    "InvalidImageError",
    "BannedError",
]


class SauceNaoError(Exception):
    """Base exception for SauceNao API errors."""

    ...


class SauceNaoServerError(SauceNaoError):
    """Exception raised when SauceNao returns a server error."""

    ...


class InvalidApiKeyError(SauceNaoError):
    """Exception raised when an invalid or wrong API key is provided."""

    ...


class RateLimitedError(SauceNaoError):
    """Exception raised when the query limit has been reached."""

    def __init__(
        self,
        limit_type: Literal["short", "daily", "invalid_requests"],
        message: str | None = None,
    ) -> None:
        self.limit_type: Literal["short", "daily", "invalid_requests"] = limit_type
        super().__init__(message or f"Rate limit reached ({limit_type} limit).")


class UploadError(SauceNaoError):
    """
    Exception raised when an error occurs during file upload.

    This can include file size errors, image dimension errors, and image processing errors.

    Requests made with remote image URL's can also raise this error if the linked image is
    too large or otherwise invalid.
    """

    ...


class FileSizeError(UploadError):
    """Exception raised when the file size is too large."""

    ...


class InvalidImageError(UploadError):
    """Exception raised when the image is invalid or cannot be processed."""

    ...


class BannedError(SauceNaoError):
    """Exception raised when the API key has been banned."""

    ...
