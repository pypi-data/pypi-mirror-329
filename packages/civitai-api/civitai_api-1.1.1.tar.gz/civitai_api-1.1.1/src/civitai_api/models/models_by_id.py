from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum
from .models import Response_Models_Type, Response_Models_Stats, Response_Models_Creator, Response_Models_modelVersion

class AllowCommercialUse(Enum):
    Image = "Image"
    RentCivit = "RentCivit"
    Rent = "Rent"
    Sell = "Sell"

class Response_Model_ById(BaseModel):
    id: int
    name: str
    description: str # html text
    allowNoCredit: bool
    allowCommercialUse: List[AllowCommercialUse]
    allowDerivatives: bool
    allowDifferentLicense: bool
    type: Response_Models_Type
    minor: bool
    poi: bool
    nsfw: bool
    nsfwLevel: int
    # cosmetic: None
    stats: Response_Models_Stats
    creator: Response_Models_Creator | None = None
    tags: List[str]
    modelVersions: List[Response_Models_modelVersion]
