from typing import TYPE_CHECKING

from pysaucenao import models
from pysaucenao.models import AccountDetails, AccountType

if TYPE_CHECKING:
    from pysaucenao.saucenao import SauceNao


__all__ = ["SauceNaoResults", "ResultFactory"]


class SauceNaoResults:
    """
    Represents the results returned from a SauceNao API query.

    Attributes:
        results (list): A list of processed results in a GenericSource inheriting
            dataclass.
        account (AccountDetails): Information about the user's SauceNao account,
            including user ID, account type, and API usage limits.
        count (int): The number of results returned by the SauceNao API.
        minimum_similarity (float): The minimum similarity score returned in the
            SauceNao results.
        response (dict): The raw response data returned by the SauceNao API.
        client (SauceNao): The client used to make the API request.
    """

    def __init__(self, response: dict, client: "SauceNao", factory: "ResultFactory"):
        self.response: dict = response
        self.client: "SauceNao" = client
        self.factory: "ResultFactory" = factory

        self._header: dict = response["header"]
        self.results: list[
            models.GenericSource
            | models.SocialSource
            | models.BooruSource
            | models.VideoSource
            | models.AnimeSource
            | models.MangaSource
        ] = self._process_results()

        self.account: AccountDetails = AccountDetails(
            user_id=int(self._header["user_id"]),
            type=AccountType(int(self._header["account_type"])),
            api_daily_limit=int(self._header["long_limit"]),
            api_short_limit=int(self._header["short_limit"]),
            api_daily_remaining=int(self._header["long_remaining"]),
            api_short_remaining=int(self._header["short_remaining"]),
        )

        self.count: int = int(self._header["results_returned"])
        self.minimum_similarity: float = float(self._header["minimum_similarity"])

    def _process_results(self):
        results = []
        for result in self.response["results"]:
            if int(result["header"]["hidden"]) == 1:
                continue
            if float(result["header"]["similarity"]) < self.client.min_similarity:
                continue
            results.append(self.factory.get_model(result))

        return results

    def __len__(self):
        return len(self.results)

    def __getitem__(self, item):
        return self.results[item]

    def __iter__(self):
        return iter(self.results)

    def __repr__(self):
        return f"SauceNaoResults(count={self.count}, results={self.results!r})"


# noinspection PyMethodMayBeStatic
class ResultFactory:
    """
    Processes raw API response data and returns the appropriate model for
    each result type.
    """

    def get_model(
        self, data: dict
    ) -> (
        models.GenericSource
        | models.SocialSource
        | models.BooruSource
        | models.VideoSource
        | models.AnimeSource
        | models.MangaSource
    ):
        match data["header"]["index_id"]:
            case 5 | 6 | 34 | 35 | 39 | 40 | 41 | 42:
                return self.social_model(data)
            case 9 | 12 | 25 | 26 | 29:
                return self.booru_model(data)
            case 21 | 22:
                return self.anime_model(data)
            case 23 | 24:
                return self.video_model(data)
            case 0 | 3 | 16 | 18 | 36 | 37:
                return self.manga_model(data)
            case _:
                return self.generic_model(data)

    def generic_model(self, data: dict) -> models.GenericSource:
        return models.GenericSource.from_api_response(data)

    def social_model(self, data: dict) -> models.SocialSource:
        return models.SocialSource.from_api_response(data)

    def booru_model(self, data: dict) -> models.BooruSource:
        return models.BooruSource.from_api_response(data)

    def video_model(self, data: dict) -> models.VideoSource:
        return models.VideoSource.from_api_response(data)

    def anime_model(self, data: dict) -> models.AnimeSource:
        return models.AnimeSource.from_api_response(data)

    def manga_model(self, data: dict) -> models.MangaSource:
        return models.MangaSource.from_api_response(data)
