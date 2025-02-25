import os
from typing import BinaryIO, IO

import aiohttp

from pysaucenao.errors import (
    SauceNaoError,
    RateLimitedError,
    InvalidApiKeyError,
    FileSizeError,
    BannedError,
    UploadError,
    InvalidImageError,
    SauceNaoServerError,
)
from pysaucenao.indexes import SauceNaoIndexes
from pysaucenao.filters import SauceNaoFilter
from pysaucenao.results import ResultFactory, SauceNaoResults

__all__ = ["SauceNao"]


class SauceNao:
    def __init__(
        self,
        api_key: str,
        *,
        indexes: SauceNaoIndexes | None = None,
        filter_level: SauceNaoFilter | None = None,
        max_results: int = 6,
        min_similarity: float = 50.0,
    ):
        self.api_key: str = api_key
        self.indexes: SauceNaoIndexes = indexes or SauceNaoIndexes().add_all()
        self.filter_level: SauceNaoFilter | None = filter_level
        self.max_results: int = max_results
        self.min_similarity: float = min_similarity
        self._endpoint: str = "https://saucenao.com/search.php"
        self._result_factory: ResultFactory = ResultFactory()

    async def from_url(self, url: str) -> SauceNaoResults:
        """
        Uploads a remote image URL to SauceNao and returns the search results.

        Args:
            url: The image URL to search for using the SauceNao API. The image will
            be downloaded by SauceNao's servers, not the library.

        Returns:
            SauceNaoResults: The results of the SauceNao search query.

        Raises:
            SauceNaoError: Raised directly if an unknown error occurs.
            SauceNaoServerError: If SauceNao returns a server error.
            RateLimitedError: If the query limit has been reached.
            InvalidApiKeyError: If the API key is invalid.
            FileSizeError: If the image file size is too large.
            BannedError: If the API key has been banned.
            UploadError: If an error occurs during file upload.
            InvalidImageError: If the image is invalid or cannot be processed
        """
        params = self._build_params()
        params["url"] = url
        async with (
            self._session() as session,
            session.get(self._endpoint, params=params) as response,
        ):
            try:
                status_code, data = response.status, await response.json()
            except aiohttp.ContentTypeError:
                raise SauceNaoServerError(
                    "SauceNao returned a malformed json response. This usually indicates a server-side error."
                )

        return self._process_response(status_code, data)

    async def from_file(
        self, path_or_fh: str | os.PathLike | BinaryIO
    ) -> SauceNaoResults:
        """
        Uploads a local image file or file-like object to SauceNao and returns the search results.

        Args:
            path_or_fh (str | os.PathLike | BinaryIO): The path to the image file or a file-like
                object containing the image to be uploaded for the search. If a
                string is provided, it is interpreted as a file path. Alternatively,
                you can provide a file-like object (BytesIO) directly.

        Returns:
            SauceNaoResults: The results of the SauceNao search query.

        Raises:
            TypeError: If the input `path_or_fh` is neither a string representing the
                file path nor a file-like object.
            SauceNaoError: Raised directly if an unknown error occurs.
            SauceNaoServerError: If SauceNao returns a server error.
            RateLimitedError: If the query limit has been reached.
            InvalidApiKeyError: If the API key is invalid.
            FileSizeError: If the image file size is too large.
            BannedError: If the API key has been banned.
            UploadError: If an error occurs during file upload.
            InvalidImageError: If the image is invalid or cannot be processed
        """

        async def _api_post(_fh: IO):
            async with (
                self._session() as session,
                session.post(self._endpoint, params=self._build_params()) as response,
            ):
                try:
                    return response.status, await response.json()
                except aiohttp.ContentTypeError:
                    raise SauceNaoServerError(
                        "SauceNao returned a malformed json response. This usually indicates a server-side error."
                    )

        if isinstance(path_or_fh, (str, os.PathLike)):
            with open(path_or_fh, "rb") as fh:
                status_code, data = await _api_post(fh)
        elif isinstance(path_or_fh, BinaryIO):
            status_code, data = await _api_post(path_or_fh)
        else:
            raise TypeError("path_or_fh must be a string or a file-like object.")

        return self._process_response(status_code, data)

    def _build_params(self) -> dict:
        """
        Constructs and returns a dictionary of API parameters.
        https://saucenao.com/user.php?page=search-api

        Returns:
            dict: A dictionary containing the compiled parameters.
        """
        params = dict()

        params["api_key"] = self.api_key
        params["dbmask"] = self.indexes.mask
        params["numres"] = self.max_results
        params["output_type"] = 2

        if self.filter_level:
            params["hide"] = self.filter_level.value

        return params

    # noinspection PyMethodMayBeStatic
    def _session(self) -> aiohttp.ClientSession:
        """
        Override this method if you need to modify how client sessions are instantiated.
        
        The "show_first" cookie is set to "0" to prevent SauceNao from overriding any
        content filters defined in the filter level.
        """
        return aiohttp.ClientSession(cookies={'show_first': '0'})

    def _process_response(self, status_code: int, response: dict) -> SauceNaoResults:
        """
        Process the raw API response data into a SauceNaoResults object.

        Args:
            status_code: The HTTP status code of the response.
            response: The raw JSON response data from the SauceNao API.

        Returns:
            SauceNaoResults: The processed results of the SauceNao search query.

        Raises:
            SauceNaoError: Raised directly if an unknown error occurs.
            SauceNaoServerError: If SauceNao returns a server error.
            RateLimitedError: If the query limit has been reached.
            InvalidApiKeyError: If the API key is invalid.
            FileSizeError: If the image file size is too large.
            BannedError: If the API key has been banned.
            UploadError: If an error occurs during file upload.
            InvalidImageError: If the image is invalid or cannot be processed
        """
        if "header" not in response or "status" not in response["header"]:
            raise SauceNaoError("Received a malformed response from SauceNao.")
        header = response["header"]

        try:
            match status_code:
                # A 200 response does not guarantee a successful search result response
                case 200:
                    if header["status"] >= 0:
                        # We got a valid search result!
                        return SauceNaoResults(response, self, self._result_factory)

                    # A 200 HTTP status code with a non-zero status code in the header indicates an error
                    match header["status"]:
                        # Account does not have API access. Likely means you've been banned. Contact SauceNao for support.
                        case -1:
                            raise BannedError(
                                header.get(
                                    "message",
                                    "This API key has been banned from use by SauceNao.",
                                )
                            )
                        # Invalid image or image processing error
                        case -3:
                            raise InvalidImageError(
                                header.get(
                                    "message",
                                    "The uploaded image is invalid or could not be processed.",
                                )
                            )
                        case -4 | -6:
                            raise UploadError(
                                header.get(
                                    "message",
                                    "The uploaded image is invalid or could not be processed.",
                                )
                            )
                        # File size too large
                        case -5:
                            raise FileSizeError(
                                header.get(
                                    "message",
                                    "The uploaded image's file size is too large.",
                                )
                            )
                        # SauceNao returned an error code we don't yet recognize
                        case _:
                            raise SauceNaoError(
                                f"SauceNao returned an unrecognized error code: {header['status']} ({header.get('message')})"
                            )
                # Rate limited
                case 429:
                    if header["status"] == -2:
                        raise RateLimitedError("invalid_requests")
                    raise RateLimitedError(
                        "short" if "every 30 seconds" in header["message"] else "daily",
                        header.get("message"),
                    )
                # Invalid API key
                case 403:
                    raise InvalidApiKeyError(
                        header.get("message", "The provided API key is invalid.")
                    )
                # File size is too large
                case 413:
                    raise FileSizeError(
                        header.get("message", "The image's file size is too large.")
                    )
                # Unknown error
                case _:
                    raise SauceNaoServerError(
                        f"SauceNao returned an unknown error code: {status_code}"
                    )
        except SauceNaoError as e:
            raise e
        except Exception as e:
            raise SauceNaoError(f"Error processing response: {e}")

    def __repr__(self):
        return f"SauceNaoClient(indexes={self.indexes.mask}, filter_level={self.filter_level}, max_results={self.max_results}, min_similarity={self.min_similarity})"
