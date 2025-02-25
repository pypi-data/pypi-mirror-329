from enum import IntEnum

__all__ = ["SauceNaoFilter"]


class SauceNaoFilter(IntEnum):
    """
    An optional explicit content filter which can be provided to the client.

    Like with most content filters, this is not foolproof and may still return
    explicit content.

    Attributes:
        NONE (int): No filtering is applied; all content is included. This is the default behavior.
        EXPLICIT (int): Attempts to filter explicit content from the results.
        POTENTIALLY_EXPLICIT (int): A more aggressive attempt to filter explicit content.
        SAFE_ONLY (int): Attempts to return only known safe content.
    """

    NONE = 0
    EXPLICIT = 1
    POTENTIALLY_EXPLICIT = 2
    SAFE_ONLY = 3
