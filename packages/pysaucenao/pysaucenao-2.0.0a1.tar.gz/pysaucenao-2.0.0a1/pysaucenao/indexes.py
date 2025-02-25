from typing import Self


__all__ = ["SauceNaoIndexes"]


# noinspection SpellCheckingInspection
class SauceNaoIndexes:
    ALL = 17592186044415

    # Common indexes
    ANIME = 0x80 | 0x100000
    H_ANIME = 0x2 | 0x200000

    PIXIV = 0x20 | 0x40
    TWITTER = 0x10000000000
    DEVIANTART = 0x200000000
    ARTSTATION = 0x4000000000
    PAWOO = 0x400000000
    FURAFFINITY = 0x8000000000
    FURRYNETWORK = 0x20000000000
    SOCIALS = (
        PIXIV | TWITTER | DEVIANTART | ARTSTATION | PAWOO | FURAFFINITY | FURRYNETWORK
    )

    # Booru indexes
    DANBOORU = 0x200
    YANDERE = 0x1000
    GELBOORU = 0x1000000
    KONACHAN = 0x2000000
    E621 = 0x10000000
    BOORUS = DANBOORU | YANDERE | GELBOORU | KONACHAN | E621

    # H-Misc Indexes
    N_HENTAI = 0x20000
    E_HENTAI = 0x2000000000
    H_MISC = N_HENTAI | E_HENTAI

    # General indexes
    H_MAGS = 0x1
    HCG = 0x4
    DDB_OBJECTS = 0x8
    DDB_SAMPLES = 0x10
    SEIGA_ILLUST = 0x100
    DRAWR = 0x400
    NIJIE = 0x800
    ANIME_OP = 0x2000
    IMDB = 0x4000
    SHUTTERSTOCK = 0x8000
    FAKKU = 0x10000
    MARKET_2D = 0x40000
    MEDIBANG = 0x80000
    MOVIES = 0x400000
    SHOWS = 0x800000
    SANKAKU = 0x4000000
    ANIME_PICTURES = 0x8000000
    IDOL_COMPLEX = 0x20000000
    BCY_ILLUST = 0x40000000
    BCY_COSPLAY = 0x80000000
    PORTAL_GRAPHICS = 0x100000000
    MADOKAMI = 0x800000000
    MANGADEX = 0x1000000000
    KEMONO = 0x40000000000
    SKEB = 0x80000000000

    def __init__(self):
        """
        A helper class for building SauceNao filters.

        By default, this class intializes with *no* indexes included. If you want to start with all indexes added and
        then remove just the ones you don't want, use the `add_all` method first.

        For example, to include all indexes except booru's,
        ```python
        indexes = SauceNaoIndexes()
        indexes.add_all().remove(index.BOORUS)
        ```

        Or to generate a filter that only includes social indexes,
        ```python
        indexes = SauceNaoIndexes()
        indexes.add(index.SOCIALS)
        ```
        """
        self._bitmask: int = 0

    @property
    def mask(self) -> int:
        """
        Returns the bitmask used for filtering SauceNao API results.

        If the generated bitmask contains _all_ currently supported indexes, we retun 999 instead.
        999 is a magic value SauceNao uses to search all indexes. Using this allows us to future-proof the library
        in the event new indexes are added later.

        Returns:
            int: The value of the bitmask.
        """
        return 999 if self._bitmask == self.ALL else self._bitmask

    def add(self, index: int) -> Self:
        self._bitmask |= index
        return self

    def add_all(self) -> Self:
        self._bitmask = self.ALL
        return self

    def remove(self, index: int) -> Self:
        self._bitmask &= ~index
        return self

    def reset(self) -> Self:
        self._bitmask = 0
        return self
