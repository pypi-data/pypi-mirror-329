import enum
from .models import Response_Models_Type as Response_Models_Type, Response_Models_modelVersions_File as Response_Models_modelVersions_File, Response_Models_modelVersions_Image as Response_Models_modelVersions_Image, Response_Models_modelVersions_Stats as Response_Models_modelVersions_Stats
from pydantic import BaseModel

class Response_ModelByVersionId_Model_Mode(enum.Enum):
    Archived = 'Archived'
    TakenDown = 'TakenDown'

class Response_ModelByVersionId_Model(BaseModel):
    name: str
    type: Response_Models_Type
    nsfw: bool
    poi: bool
    mode: Response_ModelByVersionId_Model_Mode | None

class Response_ModelByVersionId_Files_Metadata_Fp(enum.Enum):
    fp16 = 'fp16'
    fp32 = 'fp32'

class Response_ModelByVersionId_Files_Metadata_Size(enum.Enum):
    full = 'full'
    pruned = 'pruned'

class Response_ModelByVersionId_Files_Metadata_Format(enum.Enum):
    SafeTensor = 'SafeTensor'
    PickleTensor = 'PickleTensor'
    Other = 'Other'

class Response_ModelByVersionId_Files_Metadata(BaseModel):
    fp: Response_ModelByVersionId_Files_Metadata_Fp | None
    size: Response_ModelByVersionId_Files_Metadata_Size | None
    format: Response_ModelByVersionId_Files_Metadata_Format | None

class Response_ModelByVersionId_Files(BaseModel):
    sizeKb: int
    pickleScanResult: str
    virusScanResult: str
    scannedAt: str | None
    metadata: Response_ModelByVersionId_Files_Metadata

class Response_ModelByVersionId(BaseModel):
    id: int
    name: str
    description: str
    baseModel: Response_ModelByVersionId_Model
    modelId: int
    createdAt: str
    updatedAt: str
    downloadUrl: str
    trainedWords: list[str]
    files: Response_Models_modelVersions_File
    stats: Response_Models_modelVersions_Stats
    images: Response_Models_modelVersions_Image
