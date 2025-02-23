from dotenv import load_dotenv
from src.civitai_api import api
from src.civitai_api.models.images import Images_API_Opts, NsfwLevel
import pytest
import httpx
import anyio
import os
pytestmark = pytest.mark.anyio

load_dotenv()

proxy = os.environ.get('PROXY', None)
api_key = os.environ.get('API_KEY', None)
print(f"Proxy: {proxy}")
print(f"API Key: {api_key}")

@pytest.fixture
def httpx_client():
    with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as client:
        yield client

@pytest.fixture
async def httpx_async_client():
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as async_client:
        yield async_client

class TestAPI_V1:
    def test_get_creators_v1(self, httpx_client):
        response = api.get_creators_v1(httpx_client)
    
    def test_get_images_v1(self, httpx_client):
        # response = api.get_images_v1(httpx_client)
        opts: Images_API_Opts = Images_API_Opts(limit=[1], nsfw=[NsfwLevel.X.value], postId=[11059742])
        response = api.get_images_v1(httpx_client,opts=opts) # when an argument takes an enum type as input, you must use it's .value property, otherwise the query paramter's string value will have a enum class name as prefix. (which isn't a valid input for API endpoint.) 
    
    def test_get_models_v1(self, httpx_client):
        response = api.get_models_v1(httpx_client)

    def test_get_model_byId_v1(self, httpx_client):
        models = api.get_models_v1(httpx_client)

        # for model in models.items:
        #     response = api.get_model_by_id_v1(httpx_client, model.id)

        response = api.get_model_by_id_v1(httpx_client, models.items[0].id)

    def test_get_model_by_versionId_v1(self, httpx_client):
        models = api.get_models_v1(httpx_client)

        # for model in models.items:
        #     for version in model.modelVersions:
        #         response = api.get_model_by_versionId_v1(httpx_client, version.id)

        version_id = models.items[0].modelVersions[0].id
        response = api.get_model_by_versionId_v1(httpx_client, version_id)
        
    def test_get_model_by_hash_v1(self, httpx_client):
        models = api.get_models_v1(httpx_client)

        # for model in models.items:
        #     for version in model.modelVersions:
        #         for file in version.files:
        #             hash = file.hashes.BLAKE3
        #             response = api.get_model_by_hash_v1(httpx_client, hash)

        hash = models.items[0].modelVersions[0].files[0].hashes.BLAKE3
        response = api.get_model_by_hash_v1(httpx_client, hash)

class TestAPI_V1_Async:
    async def test_async_get_creators_v1(self, httpx_async_client):
        response = await api.async_get_creators_v1(httpx_async_client)

    async def test_async_get_images_v1(self, httpx_async_client):
        response = await api.async_get_images_v1(httpx_async_client)

    async def test_async_get_models_v1(self, httpx_async_client):
        response = await api.async_get_models_v1(httpx_async_client)

    async def test_async_get_model_byId_v1(self, httpx_async_client):
        models = await api.async_get_models_v1(httpx_async_client)

        # for model in models.items:
        #     response = await api.async_get_model_by_id_v1(httpx_async_client, model.id)

        response = await api.async_get_model_by_id_v1(httpx_async_client, models.items[0].id)

    async def test_async_get_model_by_versionId_v1(self, httpx_async_client):
        models = await api.async_get_models_v1(httpx_async_client)

        # for model in models.items:
        #     for version in model.modelVersions:
        #         response = await api.async_get_model_by_versionId_v1(httpx_async_client, version.id)

        version_id = models.items[0].modelVersions[0].id
        response = await api.async_get_model_by_versionId_v1(httpx_async_client, version_id)

    async def test_async_get_model_by_hash_v1(self, httpx_async_client):
        models = await api.async_get_models_v1(httpx_async_client)

        # for model in models.items:
        #     for version in model.modelVersions:
        #         for file in version.files:
        #             hash = file.hashes.BLAKE3
        #             response = await api.async_get_model_by_hash_v1(httpx_async_client, hash)

        hash = models.items[0].modelVersions[0].files[0].hashes.BLAKE3
        response = await api.async_get_model_by_hash_v1(httpx_async_client, hash)