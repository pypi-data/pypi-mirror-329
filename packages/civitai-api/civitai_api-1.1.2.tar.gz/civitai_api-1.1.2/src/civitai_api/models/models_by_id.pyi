from .models import Response_Models_Creator as Response_Models_Creator, Response_Models_Stats as Response_Models_Stats, Response_Models_Type as Response_Models_Type, Response_Models_modelVersion as Response_Models_modelVersion
from enum import Enum
from pydantic import BaseModel

class AllowCommercialUse(Enum):
    Image = 'Image'
    RentCivit = 'RentCivit'
    Rent = 'Rent'
    Sell = 'Sell'

class Response_Model_ById(BaseModel):
    id: int
    name: str
    description: str
    allowNoCredit: bool
    allowCommercialUse: list[AllowCommercialUse]
    allowDerivatives: bool
    allowDifferentLicense: bool
    type: Response_Models_Type
    minor: bool
    poi: bool
    nsfw: bool
    nsfwLevel: int
    stats: Response_Models_Stats
    creator: Response_Models_Creator | None
    tags: list[str]
    modelVersions: list[Response_Models_modelVersion]
