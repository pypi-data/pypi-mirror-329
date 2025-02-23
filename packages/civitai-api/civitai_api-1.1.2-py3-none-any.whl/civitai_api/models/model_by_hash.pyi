from .model_by_version_id import Response_ModelByVersionId as Response_ModelByVersionId
from pydantic import BaseModel as BaseModel

class Response_Model_ByHash(Response_ModelByVersionId):
    class Config:
        orm_mode: bool
