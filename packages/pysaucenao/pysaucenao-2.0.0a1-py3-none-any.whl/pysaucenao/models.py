import re
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Self

__all__ = [
    "INDEXES",
    "GenericSource",
    "SocialSource",
    "BooruSource",
    "VideoSource",
    "AnimeSource",
    "MangaSource",
    "AccountDetails",
    "AccountType",
]

INDEXES = {
    0: "H-Magazines",
    2: "H-Game CG",
    3: "DoujinshiDB",
    5: "Pixiv",
    6: "Pixiv (Historical)",
    8: "Nico Nico Seiga",
    9: "Danbooru",
    10: "drawr Images",
    11: "Nijie Images",
    12: "Yande.re",
    15: "Shutterstock",
    16: "FAKKU",
    18: "H-Misc",
    19: "2D-Market",
    20: "MediBang",
    21: "Anime",
    22: "H-Anime",
    23: "Movies",
    24: "Shows",
    25: "Gelbooru",
    26: "Konachan",
    27: "Sankaku Channel",
    28: "Anime-Pictures.net",
    29: "e621.net",
    30: "Idol Complex",
    31: "bcy.net Illust",
    32: "bcy.net Cosplay",
    33: "PortalGraphics.net (Hist)",
    34: "deviantArt",
    35: "Pawoo.net",
    36: "Madokami (Manga)",
    37: "MangaDex",
    38: "E-Hentai",
    39: "ArtStation",
    40: "FurAffinity",
    41: "Twitter",
    42: "Furry Network",
    43: "Kemono",
    44: "Skeb",
}


@dataclass(kw_only=True)
class GenericSource:
    """
    Represents a generic source retrieved from SauceNao. All other source classes inherit from this class
    and provide access to the same basic data.

    Attributes:
        similarity (float): The similarity score of the uploaded image when compared to the original source image.
            This value is represented as a float with a range of 0.0 to 100.0. Image compression, cropping and edits
            will all negatively impact the similarity score, but a score above 80.0 is a fairly confident match.
        thumbnail (str): A temporarily accessible signed thumbnail URL. Not suitable for anything but temporary use.
            This is the thumbnail for what SauceNao believes is the source of your image. It is not necessarily a
            thumbnail of the image you uploaded.
        index (str): The human-readable name of the index the source belongs to.
        index_id (int): The unique numeric identifier of the index.
        index_name (str): The detailed name of the index. Includes the index ID, index name and filename.
        author_name (str | None): The name of the primary author associated with the source, if available.
        authors (list): A list of all authors associated with the source. This may be an empty list.
        author_url (str | None): The URL pointing to the author's profile, if available.
        title (str | None): The title or name of the source material, if available.
        url (str | None): The primary URL where the source content can be found, if available.
        urls (list): A list of URLs associated with the source. This may be an empty list.
    """

    similarity: float
    thumbnail: str
    index: str
    index_id: int
    index_name: str
    author_name: str | None = None
    authors: list = field(default_factory=list)
    author_url: str | None = None
    title: str | None = None
    url: str | None = None
    urls: list = field(default_factory=list)
    # self.created_at:    typing.Optional[datetime] = None

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        header = response["header"]
        data = response["data"]

        fields = {
            "similarity": float(header["similarity"]),
            "thumbnail": header["thumbnail"],
            "index": INDEXES.get(int(header["index_id"])),
            "index_id": int(header["index_id"]),
            "index_name": header["index_name"],
            "authors": [],
            "urls": [],
        }

        # Override the index for Kemono to use the actual service name (Patreon or Fanbox)
        if fields["index_id"] == 43:
            fields["index"] = data.get("service_name", fields["index"])

        # Depending on the index, our title can come from a variety of different fields.
        for key in ["title", "eng_name", "material", "source"]:
            if key in data:
                fields["title"] = data[key]
                break

        # Like the title, the author fields vary from index to index
        for key in ["member_name", "creator", "author_name", "author"]:
            if key in data:
                author_field = data[key]
                if key == "creator" and isinstance(author_field, list):
                    fields["author_name"] = author_field[0]
                    fields["authors"] = author_field
                else:
                    fields["author_name"] = author_field
                    fields["authors"] = [author_field]
                break

        # The author URL is actually the ext URL for pawoo indexes
        if "author_url" in data:
            fields["author_url"] = data["author_url"]
        elif "pawoo_id" in data and "ext_urls" in data:
            fields["author_url"] = data["ext_urls"][0]

        # The URL to where the content was posted, if applicable for this index
        if "ext_urls" in data:
            fields["url"] = data["ext_urls"][0]
            fields["urls"] = data["ext_urls"]

        return cls(**fields)


@dataclass(kw_only=True)
class SocialSource(GenericSource):
    """
    Represents a social media source of an image.

    This includes common sources such as Pixiv, Twitter, Deviantart and FurAffinity.

    Attributes:
        post_id (int | None): The unique identifier of the social media post, if available.
        user_id (int | None): The unique identifier for the user associated with
            the social media account, if available.
    """

    post_id: int | None = None
    user_id: int | None = None

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        source = super().from_api_response(response)  # type: Self

        match source.index_id:
            case 5 | 6:  # Pixiv
                source.post_id = response["data"].get("pixiv_id")
                source.user_id = response["data"].get("member_id")
            case 34:  # Deviantart
                source.post_id = response["data"].get("da_id")
            case 35:  # Pawoo
                source.post_id = response["data"].get("pawoo_id")
                source.author_name = response["data"].get("pawoo_user_username")
            case 40:  # FurAffinity
                source.post_id = response["data"].get("fa_id")
            case 41:  # Twitter
                source.post_id = response["data"].get("tweet_id")
                source.user_id = response["data"].get("twitter_user_id")
                source.author_name = response["data"].get("twitter_user_handle")
            case 42:  # Furry Network
                source.post_id = response["data"].get("fn_id")

        return source


@dataclass(kw_only=True)
class BooruSource(GenericSource):
    """
    Represents a booru source (such as Gelbooru or Danbooru).

    Booru's are often excellent ways to find the original sources of images when other indexes fail.

    Attributes:
        characters (list[str]): A list of characters present in the image, if available. This may be an empty list.
        material (list[str]): A list of materials present in the image (e.g. the game or anime the characters are from).
            Like characters, this may also be an empty list.
    """

    characters: list[str] = field(default_factory=list)
    material: list[str] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        source = super().from_api_response(response)  # type: Self

        characters = response["data"].get("characters")
        if characters:
            source.characters = characters.replace(", ", ",").split(",")

        material = response["data"].get("material")
        if material:
            source.material = material.replace(", ", ",").split(",")

        # Extract the source URL provided by the booru if it's available
        urls = response["data"].get("ext_urls") or []
        source_url = response["data"].get("source")
        if source_url:
            source_url = cls._format_source_url(source_url)
            source.url = source_url
            urls = [source_url] + urls
        source.urls = urls

        return source

    @staticmethod
    def _format_source_url(url: str):
        """
        SauceNao's API often returns a hot-linked image URL for Pixiv sources.
        These URL's cannot be followed and will result in 403 errors.

        However, we can easily fix this by extracting the post ID from the image URL and rewriting it ourselves.
        So, for example,
        `https://i.pximg.net/img-original/img/2020/01/01/10/25/45/123456789`
        Would become,
        `https://www.pixiv.net/artworks/123456789`
        """
        matches = re.search(
            r"^https?://i\.pximg\.net/img-original/img/[\d/]+/(?P<id>\d+)$", url
        )
        if matches:
            return f"https://www.pixiv.net/artworks/{matches.group('id')}"

        return url


@dataclass(kw_only=True)
class VideoSource(GenericSource):
    """
    Represents a video source, such as an anime or movie.

    Attributes:
        episode (int | None): The episode number associated with the video source, if available.
        timestamp (str | None): The timestamp of the video source if available, typically
            provided in a "00:00:00 / 00:00:00" format.
        year (int | None): The year associated with the video source if available. It can be
            a standalone year (e.g. "1996"), or a year range (e.g. "1998-2001")
    """

    episode: int | None = None
    timestamp: str | None = None
    year: int | None = None

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        source = super().from_api_response(response)  # type: Self

        source.episode = response["data"].get("part")
        source.timestamp = response["data"].get("est_time")
        year = response["data"].get("year")
        if year:
            # Years can either be a range (e.g. "1998-2001"), or a single year. Sometimes single years end up having an
            # unneeded "-" at the end (e.g. "1996-"), so this just applies a minor formatting fix.
            source.year = year.rstrip("-")

        return source


@dataclass(kw_only=True)
class AnimeSource(VideoSource):
    """
    Represents an anime video source.

    Attributes:
        anidb_id (int | None): AniDB unique identifier for the anime, if available.
        anidb_url (str | None): URL to the AniDB page for the anime, if available.
        mal_id (int | None): MyAnimeList unique identifier for the anime, if available.
        mal_url (str | None): URL to the MyAnimeList page for the anime, if available.
        anilist_id (int | None): AniList unique identifier for the anime, if available.
        anilist_url (str | None): URL to the AniList page for the anime, if available.
    """

    anidb_id: int | None = None
    anidb_url: str | None = None
    mal_id: int | None = None
    mal_url: str | None = None
    anilist_id: int | None = None
    anilist_url: str | None = None

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        source = super().from_api_response(response)  # type: Self

        source.anidb_id = response["data"].get("anidb_aid")
        if source.anidb_id:
            source.anidb_url = f"https://anidb.net/anime/{source.anidb_id}"

        source.mal_id = response["data"].get("mal_id")
        if source.mal_id:
            source.mal_url = f"https://myanimelist.net/anime/{source.mal_id}"

        source.anilist_id = response["data"].get("anilist_id")
        if source.anilist_id:
            source.anilist_url = f"https://anilist.co/anime/{source.anilist_id}"

        return source


@dataclass(kw_only=True)
class MangaSource(GenericSource):
    """
    Represents a manga source.

    Attributes:
        chapter (str | None): The chapter of the manga, if available.
        artist (str | None): The artist of the manga, if available. A manga series may have a different artist
        and author.
    """

    chapter: str | None = None
    artist: str | None = None

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        source = super().from_api_response(response)  # type: Self

        part = response["data"].get("part")
        if part:
            source.chapter = part.lstrip("- ")

        source.artist = response["data"].get("artist")

        if "eng_name" in response["data"]:
            source.title = response["data"]["eng_name"]
        elif "source" in response["data"]:
            source.title = response["data"]["source"]

        return source


@dataclass(kw_only=True)
class AccountDetails:
    user_id: int
    type: "AccountType"
    api_daily_limit: int
    api_short_limit: int
    api_daily_remaining: int
    api_short_remaining: int


class AccountType(IntEnum):
    GUEST = 0
    FREE = 1
    ENHANCED = 2

    @classmethod
    def _missing_(cls, value):
        return cls.GUEST
