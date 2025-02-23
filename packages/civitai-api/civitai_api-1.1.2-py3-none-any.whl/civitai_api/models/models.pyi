import enum
from .images import Period as Period
from _typeshed import Incomplete
from pydantic import BaseModel, Strict as Strict, StrictBool as StrictBool, StrictInt as StrictInt
from typing import Annotated, Any

class Response_Models_Type(enum.Enum):
    Checkpoint = 'Checkpoint'
    TextualInversion = 'TextualInversion'
    Hypernetwork = 'Hypernetwork'
    AestheticGradient = 'AestheticGradient'
    LORA = 'LORA'
    Controlnet = 'Controlnet'
    Poses = 'Poses'
    LoCon = 'LoCon'
    DoRA = 'DoRA'
    Other = 'Other'
    MotionModule = 'MotionModule'
    Upscaler = 'Upscaler'
    VAE = 'VAE'
    Wildcards = 'Wildcards'
    Workflows = 'Workflows'

class Response_Models_Mode(enum.Enum):
    Archived = 'Archived'
    TakenDown = 'TakenDown'

class Response_Models_Creator(BaseModel):
    username: str
    image: str | None

class Response_Models_Stats(BaseModel):
    downloadCount: int
    favoriteCount: int
    thumbsUpCount: int
    thumbsDownCount: int
    commentCount: int
    ratingCount: int
    rating: float
    tippedAmountCount: int

class Response_Models_modelVersions_Files_Metadata_fp(enum.Enum):
    fp8 = 'fp8'
    fp16 = 'fp16'
    fp32 = 'fp32'

class Response_Models_modelVersions_Files_Metadata_Size(enum.Enum):
    full = 'full'
    pruned = 'pruned'

class Response_Models_modelVersions_Files_Metadata_Format(enum.Enum):
    SafeTensor = 'SafeTensor'
    PickleTensor = 'PickleTensor'
    Other = 'Other'
    Diffusers = 'Diffusers'

class Response_Models_modelVersions_Files_Metadata(BaseModel):
    fp: Response_Models_modelVersions_Files_Metadata_fp | None
    size: Response_Models_modelVersions_Files_Metadata_Size | None
    format: Response_Models_modelVersions_Files_Metadata_Format | None

class Response_Models_modelVersions_Files_PickleScanResult(enum.Enum):
    Pending = 'Pending'
    Success = 'Success'
    Danger = 'Danger'
    Error = 'Error'

class Response_Models_modelVersions_Files_VirusScanResult(enum.Enum):
    Pending = 'Pending'
    Success = 'Success'
    Danger = 'Danger'
    Error = 'Error'

class Response_Models_modelVersions_Files_Hashes(BaseModel):
    SHA256: str | None
    CRC32: str | None
    BLAKE3: str | None
    AutoV3: str | None

class Response_Models_modelVersions_File(BaseModel):
    name: str
    id: int
    sizeKb: float | None
    metadata: Response_Models_modelVersions_Files_Metadata
    pickleScanResult: Response_Models_modelVersions_Files_PickleScanResult
    virusScanResult: Response_Models_modelVersions_Files_VirusScanResult
    scannedAt: str | None
    hashes: Response_Models_modelVersions_Files_Hashes
    downloadUrl: str
    primary: bool | None

class Response_Models_modelVersions_Images_Meta(BaseModel):
    ENSD: str | None
    Size: str | None
    seed: int | None
    Score: str | None
    steps: int | None
    prompt: str | None
    sampler: str | None
    Eta_DDIM: str | None
    cfgScale: float | None
    resources: list[Any] | None
    Model_hash: str | None
    Hires_upscale: str | None
    Hires_upscaler: str | None
    negativePrompt: str | None
    Denoising_strength: str | None

class Response_Models_modelVersions_Image(BaseModel):
    url: str
    nsfwLevel: int
    width: int
    height: int
    hash: str
    meta: Response_Models_modelVersions_Images_Meta | None

class Response_Models_modelVersions_Stats(BaseModel):
    downloadCount: int
    ratingCount: int
    rating: float

class Response_Models_modelVersions_Model(BaseModel):
    name: str
    type: Response_Models_Type
    nsfw: bool
    poi: bool

class Response_Models_modelVersion(BaseModel):
    id: int
    modelId: int | None
    baseModel: str
    name: str
    earlyAccessEndsAt: str | None
    earlyAccessConfig: dict[str, Any] | None
    uploadType: str | None
    description: str | None
    createdAt: str | None
    updatedAt: str | None
    status: str | None
    publishedAt: str
    downloadUrl: str
    trainedWords: list[str] | None
    files: list[Response_Models_modelVersions_File]
    images: list[Response_Models_modelVersions_Image] | None
    stats: Response_Models_modelVersions_Stats

class Response_Models_Metadata(BaseModel):
    totalItems: int | None
    currentPage: int | None
    pageSize: int | None
    totalPages: int | None
    nextPage: str | None
    prevPage: str | None

class Response_Model(BaseModel):
    id: int
    name: str
    description: str
    type: Response_Models_Type | None
    nsfw: bool
    tags: list[str]
    mode: Response_Models_Mode | None
    creator: Response_Models_Creator | None
    stats: Response_Models_Stats
    modelVersions: list[Response_Models_modelVersion]

class Response_Models(BaseModel):
    items: list[Response_Model]
    metadata: Response_Models_Metadata

class Sort(enum.Enum):
    Highest_Rated = 'Highest Rated'
    Most_Downloaded = 'Most Downloaded'
    Newest = 'Newest'

class AllowCommercialUse(enum.Enum):
    None_ = 'None'
    Image = 'Image'
    Rent = 'Rent'
    Sell = 'Sell'

LimitInt: Incomplete
Limit: Incomplete

class Models_API_Opts(BaseModel):
    limit: None | Limit
    page: None | Annotated[list[StrictInt], None]
    query: None | Annotated[list[str], None]
    tag: None | Annotated[list[str], None]
    username: str | None
    types: list[Response_Models_Type] | None
    sort: None | Annotated[list[Sort], None]
    period: None | Annotated[list[Period], None]
    favorites: None | Annotated[list[StrictBool], None]
    hidden: None | Annotated[list[StrictBool], None]
    primaryFileOnly: None | Annotated[list[StrictBool], None]
    allowNoCredit: None | Annotated[list[StrictBool], None]
    allowDerivatives: None | Annotated[list[StrictBool], None]
    allowDifferentLicenses: None | Annotated[list[StrictBool], None]
    allowCommercialUse: list[AllowCommercialUse] | None
    nsfw: None | Annotated[list[StrictBool], None]
    supportsGeneration: None | Annotated[list[StrictBool], None]
