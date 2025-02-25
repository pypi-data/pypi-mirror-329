# pySauceNao

pySauceNao is an unofficial asynchronous library for the [SauceNao](https://saucenao.com/) API. It supports lookups via remote URL's or uploads from the local filesystem.

# Installation
This library requires [Python 3.11](https://www.python.org) or above.

You can install the library through pip as follows,
```shell script
pip install pysaucenao
```

# Basic usage
Make sure you have obtained an API key from [SauceNao](https://saucenao.com/user.php?page=search-api) first.

The following example demonstrates how to use the library to perform a lookup on a remote image file,

```python
import asyncio
from pysaucenao import SauceNao

sauce = SauceNao(api_key='your_api_key')
results = asyncio.run(sauce.from_url('https://m.media-amazon.com/images/S/pv-target-images/4e34528d6934e91a4ab5120af64ba86ca0315eec83fc68e63b376b15aa136c10.png'))
for result in results:
    print(f"Title: {result.title} ({result.similarity}% match)")
    print(f"Author: {result.author_name}")
    print(f"Link: {result.url}\n")
```

Some search results, such as anime search results, can contain additional information such as episode numbers, timestamps and so on.

```python
import asyncio
from pysaucenao import SauceNao, AnimeSource

sauce = SauceNao(api_key='your_api_key')
results = asyncio.run(sauce.from_url('https://m.media-amazon.com/images/S/pv-target-images/4e34528d6934e91a4ab5120af64ba86ca0315eec83fc68e63b376b15aa136c10.png'))
if isinstance(results[0], AnimeSource):
    print(f"Title: {results[0].title}")
    print(f"Timestamp: {results[0].timestamp}")
```

# Filtering

## Index filtering
By default, SauceNao executes search queries on all indexes. 

To limit your search to specific ones, build a list of indexes using the `SauceNaoIndexes` class and pass it to the `SauceNao` constructor.

For example, to only include search results from the social media indexes (such as Pixiv, Twitter, DeviantArt and so on), you can do the following,
```python
from pysaucenao import SauceNao, SauceNaoIndexes
indexes = SauceNaoIndexes().add(SauceNaoIndexes.SOCIALS)
sauce = SauceNao(api_key='your_api_key', indexes=indexes)
```

To exclude specific indexes, make sure to call the `add_all` method first,
```python
from pysaucenao import SauceNaoIndexes
indexes = SauceNaoIndexes().add_all().remove(SauceNaoIndexes.H_MISC)
```

For a full list of indexes, refer to the `SauceNaoIndexes` class.

## Explicit content filtering
SauceNao's API provides an option to attempt to filter out explicit content from search results.

By default, pySauceNao does not apply any filtering.

If you wish to enable explicit content filtering, you can specify a filter level when constructing the `SauceNao` object,
```python
from pysaucenao import SauceNao, SauceNaoFilter
sauce = SauceNao(api_key='your_api_key', filter_level=SauceNaoFilter.SAFE_ONLY)
```

`SAFE_ONLY` is the most aggressive filtering level, which attempts to only return results that SauceNao believes are "safe-for-work". 

The other two options are `EXPLICIT`, which only filters results SauceNao has a high confidence are explicit, and `POTENTIALLY_EXPLICIT` which offers a middle ground in-between `EXPLICIT` and `SAFE_ONLY`.


# Error handling

pySauceNao raises a `SauceNaoError` if an error occurs while executing an API query.

The following exceptions are subclasses of `SauceNaoError` and allow you to handle specific errors,
- `SauceNaoServerError`: The SauceNao server is currently down.
- `InvalidApiKeyError`: The API key you provided is invalid.
- `RateLimitedError`: You have exceeded your search query limit. Provides a `limit_type` attribute that is either `short`, `daily`, or `invalid_requests`.
  - `short`: You have exceeded your 30-second search query limit.
  - `daily`: You have exceeded your 24-hour search query limit.
  - `invalid_requests`: You have made too many invalid requests in a short time period.
- `UploadError`: The image provided was too large or not a valid image. You can also catch more specific `UploadError` exceptions,
  - `FileSizeError`: The image was too large.
  - `InvalidImageError`: The image was not a valid image.
- `BannedError`: The API key you provided has been banned from use.

