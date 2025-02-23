# civitai_api

This project provide a easy way to communicating with Civitai-API.

It supports both Sync and Async request implementation, and both Async implementation (AsyncIO and Trio) by using Anyio.

## usage

this was designed to be a flexale library, which only need you initialize an httpx library as the function's first argument.

### 0. Initialize an CivitaiAPI class

```python
from civitai_api.api import CivitaiAPI

civitai_api = CivitaiAPI(api_key="xxxxxxxx")

```

To register your own api key, see [here](https://github.com/civitai/civitai/wiki/REST-API-Reference#authorization).

#### Or initialize an httpx client (or async httpx client) and use with functions.

for Sync Clinet:

```python
from civitai_api import api
import httpx

proxy = "http://127.0.0.1:7890"

# setting up your civitai api key and proxy
client = httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy)
# or 
with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as client:
    ......
```

For Async Client:

```python
async_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy)
# or 
async with httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as async_client:
    ......
```

> for more info please checkout [httpx official website](https://www.python-httpx.org/advanced/clients/).

### 2. request for certain endpoint

For a certain endpoint, there will have two functions for both sync and async implementation. And the only two differences between them were:

1. the async implementation's first argument takes async httpx client instance.
2. async implementation's function name will have 'async_' as the prefix to differenciate whether it's Sync or Async.

to be supplemented.

### 3. how to correctly write arguments

For endpoints: creators, images and models, there are 3 functions (and 3 async implementatons) takes function arguments to construct request query paramters.

and every argument value have to be enclosed by a list:

```python
opts: Images_API_Opts = Images_API_Opts(limit=[1], nsfw=[NsfwLevel.X.value], postId=[11059742])
response = api.get_images_v1(httpx_client,opts=opts)
```

That's because the httpx library have it's own way to construct query paramters.

> for more info: [query-parameters](https://www.python-httpx.org/compatibility/#query-parameters)

#### for some arguments those takes List[enum] type as input

You should always take care of when an argument takes a specific enum type as input.
For example the ["images"](https://github.com/civitai/civitai/wiki/REST-API-Reference#response-fields-1) endpoint can take nsfw as input, And I make every nsfw level option into a NsfwLevel enum type, when you want specific the nsfw level filter you should write like this: 

```python
from civitai_api.models.images import NsfwLevel

......# after initialize httpx client

opts: Images_API_Opts = Images_API_Opts(limit=[1], nsfw=[NsfwLevel.X.value], postId=[11059742]) 
# Do This: nsfw=[NsfwLevel.X.value]
# Do Not: nsfw=[NsfwLevel.X]
```

When an argument takes an enum type as input, you must use the 'value' property from an enum field like this:

```python
nsfw=[NsfwLevel.X.value]
```

Otherwise the query paramter's string value will have a enum class name as prefix. (which isn't a valid input for API endpoint.)
