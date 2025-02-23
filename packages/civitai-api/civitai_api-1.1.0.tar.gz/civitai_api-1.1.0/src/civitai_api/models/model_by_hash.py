from .model_by_version_id import Response_ModelByVersionId
from pydantic import BaseModel

class Response_Model_ByHash(Response_ModelByVersionId):
    class Config:
        orm_mode = True