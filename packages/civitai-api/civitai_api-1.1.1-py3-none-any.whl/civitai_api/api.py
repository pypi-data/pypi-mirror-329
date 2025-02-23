import enum
from typing import Any, List, Optional, Coroutine, Dict
import anyio.from_thread
import httpx
from civitai_api.models.creators import Response_Creaters, Creators_API_Opts
from civitai_api.models.images import Images_API_Opts, NsfwLevel, Period, Response_Images
from civitai_api.models.models import Models_API_Opts, Response_Models, Response_Models_Type, Response_Models_modelVersion
from civitai_api.models.model_by_version_id import Response_ModelByVersionId
import anyio
import os
from urllib.parse import urljoin

from civitai_api.models.models_by_id import Response_Model_ById

# API endpoints references: https://github.com/civitai/civitai/wiki/REST-API-Reference

API_URL_V1 = "https://civitai.com/api/v1/"
API_URL_V1_Creators = urljoin(API_URL_V1, "creators") # https://civitai.com/api/v1/creators
API_URL_V1_Images = urljoin(API_URL_V1, "images") # https://civitai.com/api/v1/images
API_URL_V1_Models = urljoin(API_URL_V1, "models") # https://civitai.com/api/v1/models
API_URL_V1_Model_By_Id = urljoin(API_URL_V1, "models/") # "https://civitai.com/api/v1/models/:modelId"
API_URL_ModelVersion_By_VersionId = urljoin(API_URL_V1, "model-versions/")  # "https://civitai.com/api/v1/model-versions/:modelVersionId"
API_URL_ModelVersion_By_Hash = urljoin(API_URL_V1, "model-versions/by-hash/") # "https://civitai.com/api/v1/model-versions/by-hash/:hash"
API_URL_Tags = urljoin(API_URL_V1, "tags") # https://civitai.com/api/v1/tags

# def construct_header_from_dict(params: dict) -> dict:
    # params.pop("self", None)
    # params.pop("httpx_client", None)
    # params.pop("httpx_async_client", None)
    # return {k: str(v) for k, v in params.items() if v is not None}

def construct_query_params_from_dict(params: Dict[str, List[Any]]):
    query_params: Dict[str, List[Any]] = {}

    for k,v in params.items():
        if params[k] == None:
            continue
        query_params[k] = []
        for item in v:
            if isinstance(item, bool):
                query_params[k].append(str(item).lower())
            else:
                query_params[k].append(str(item))
    
    return query_params
    
# def is_running_anyio_loop():
#     try:
#         # Attempt to get the current task
#         anyio.get_current_task()
#         return True  # If successful, an AnyIO event loop is running
#     except RuntimeError:
#         return False  # No running AnyIO event loop

def get_creators_v1(
        httpx_client:httpx.Client,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx.get(API_URL_V1_Creators, params=query_params)
    return Response_Creaters(**response.json())

async def async_get_creators_v1(
        httpx_async_client:httpx.AsyncClient,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Creators, params=query_params)
    return Response_Creaters(**response.json())

def get_images_v1(
        httpx_client:httpx.Client,
        opts: Images_API_Opts | None = None
        ) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_V1_Images, params=query_params)
    return Response_Images(**response.json())

async def async_get_images_v1(
        httpx_async_client:httpx.AsyncClient,
        opts: Images_API_Opts | None = None
) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Images, params=query_params)
    return Response_Images(**response.json())

def get_models_v1(
        httpx_client:httpx.Client,
        opts: Models_API_Opts | None = None
) -> Response_Models:
    if (opts):
        if (opts.favorites or opts.hidden):
            if not (httpx_client.headers):
                raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_V1_Models, params=query_params)
    return Response_Models(**response.json())

async def async_get_models_v1(
        httpx_async_client:httpx.AsyncClient,
        opts: Models_API_Opts | None = None
) -> Response_Models:
    if (opts):
        if (opts.favorites or opts.hidden):
            if not (httpx_async_client.headers):
                raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Models, params=query_params)
    return Response_Models(**response.json())

def get_model_by_id_v1(
        httpx_client:httpx.Client,
        modelId: int
) -> Response_Model_ById:
    response = httpx_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    return Response_Model_ById(**response.json())

async def async_get_model_by_id_v1(
        httpx_async_client:httpx.AsyncClient,
        modelId: int
) -> Response_Model_ById:
    response = await httpx_async_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    return Response_Model_ById(**response.json())

def get_model_by_versionId_v1(
        httpx_client:httpx.Client,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    return Response_Models_modelVersion(**response.json())

async def async_get_model_by_versionId_v1(
        httpx_async_client:httpx.AsyncClient,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = await httpx_async_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    return Response_Models_modelVersion(**response.json())

def get_model_by_hash_v1(
        httpx_client:httpx.Client,
        hash: str
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    return Response_Models_modelVersion(**response.json())

async def async_get_model_by_hash_v1(
        httpx_async_client:httpx.AsyncClient,
        hash: str
) -> Response_Models_modelVersion:
    response = await httpx_async_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    return Response_Models_modelVersion(**response.json())

class CivitaiAPI:
    def __init__(self, api_key: str, proxy: str | None = None):
        self.api_key = api_key
        self.proxy = proxy
        self.httpx_client = httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy)
        self.httpx_async_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy)

    def get_creators_v1(self, opts: Creators_API_Opts | None = None) -> Response_Creaters:
        return get_creators_v1(self.httpx_client, opts)
    
    async def async_get_creators_v1(self, opts: Creators_API_Opts | None = None) -> Response_Creaters:
        return await async_get_creators_v1(self.httpx_async_client, opts)
    
    def get_images_v1(self, opts: Images_API_Opts | None = None) -> Response_Images:
        return get_images_v1(self.httpx_client, opts)
    
    async def async_get_images_v1(self, opts: Images_API_Opts | None = None) -> Response_Images:
        return await async_get_images_v1(self.httpx_async_client, opts)
    
    def get_models_v1(self, opts: Models_API_Opts | None = None) -> Response_Models:
        return get_models_v1(self.httpx_client, opts)
    
    async def async_get_models_v1(self, opts: Models_API_Opts | None = None) -> Response_Models:
        return await async_get_models_v1(self.httpx_async_client, opts)
    
    def get_model_by_id_v1(self, modelId: int) -> Response_Model_ById:
        return get_model_by_id_v1(self.httpx_client, modelId)
    
    async def async_get_model_by_id_v1(self, modelId: int) -> Response_Model_ById:
        return await async_get_model_by_id_v1(self.httpx_async_client, modelId)
    
    def get_model_by_versionId_v1(self, modelVersionId: int) -> Response_Models_modelVersion:
        return get_model_by_versionId_v1(self.httpx_client, modelVersionId)
    
    async def async_get_model_by_versionId_v1(self, modelVersionId: int) -> Response_Models_modelVersion:
        return await async_get_model_by_versionId_v1(self.httpx_async_client, modelVersionId)
    
    def get_model_by_hash_v1(self, hash: str) -> Response_Models_modelVersion:
        return get_model_by_hash_v1(self.httpx_client, hash)
    
    async def async_get_model_by_hash_v1(self, hash: str) -> Response_Models_modelVersion:
        return await async_get_model_by_hash_v1(self.httpx_async_client, hash)
    