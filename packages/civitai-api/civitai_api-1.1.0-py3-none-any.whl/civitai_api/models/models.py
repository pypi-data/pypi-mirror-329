from typing import List, Dict, Any, Optional, Annotated
from annotated_types import Len
from pydantic import BaseModel, Field, Strict, StrictBool, StrictInt
import enum
from .images import Period

class Response_Models_Type(enum.Enum):
    Checkpoint = "Checkpoint"
    TextualInversion = "TextualInversion"
    Hypernetwork = "Hypernetwork"
    AestheticGradient = "AestheticGradient"
    LORA = "LORA"
    Controlnet = "Controlnet"
    Poses = "Poses"
    LoCon = "LoCon"
    DoRA = "DoRA"
    Other = "Other"
    MotionModule = "MotionModule"
    Upscaler = "Upscaler"
    VAE = "VAE"
    Wildcards = "Wildcards"
    Workflows = "Workflows"

class Response_Models_Mode(enum.Enum):
    Archived = "Archived"
    TakenDown = "TakenDown"

class Response_Models_Creator(BaseModel):
    username: str 	# The name of the creator
    image: str | None 	# The url of the creators avatar

class Response_Models_Stats(BaseModel):
    downloadCount: int # The number of downloads the model has
    favoriteCount: int # The number of favorites the model has
    thumbsUpCount: int # The number of thumbs up the model has
    thumbsDownCount: int # The number of thumbs down the model has
    commentCount: int # The number of comments the model has
    ratingCount: int # The number of ratings the model has
    rating: float	# The average rating of the model
    tippedAmountCount: int # The number of tips the model has

class Response_Models_modelVersions_Files_Metadata_fp(enum.Enum):
    fp8 = "fp8"
    fp16 = "fp16"
    fp32 = "fp32"

class Response_Models_modelVersions_Files_Metadata_Size(enum.Enum):
    full = "full"
    pruned = "pruned"

class Response_Models_modelVersions_Files_Metadata_Format(enum.Enum):
    SafeTensor = "SafeTensor"
    PickleTensor = "PickleTensor"
    Other = "Other"
    Diffusers = "Diffusers"

class Response_Models_modelVersions_Files_Metadata(BaseModel):
    fp: Response_Models_modelVersions_Files_Metadata_fp | None = None # The specified floating point for the file
    size: Response_Models_modelVersions_Files_Metadata_Size | None = None # The specified model size for the file
    format: Response_Models_modelVersions_Files_Metadata_Format | None = None 	# The specified model format for the file


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
    # AutoV2: str | None = None
    SHA256: str | None = None
    CRC32: str | None = None
    BLAKE3: str | None = None
    AutoV3: str | None = None

class Response_Models_modelVersions_File(BaseModel):
    name: str # file name
    id: int # file id
    sizeKb: float | None = None # The size of the model file
    metadata: Response_Models_modelVersions_Files_Metadata
    pickleScanResult: Response_Models_modelVersions_Files_PickleScanResult # Status of the pickle scan ('Pending', 'Success', 'Danger', 'Error')
    virusScanResult: Response_Models_modelVersions_Files_VirusScanResult # Status of the virus scan ('Pending', 'Success', 'Danger', 'Error')
    scannedAt: str | None = None # (ISO 8601) The date in which the file was scanned
    hashes: Response_Models_modelVersions_Files_Hashes
    downloadUrl: str # model download url: "https://civitai.com/api/download/models/8387"
    primary: bool | None = None # If the file is the primary file for the model version

class Response_Models_modelVersions_Images_Meta(BaseModel):
    ENSD: str | None = None # stringified number
    Size: str | None = None # resolution string 
    seed: int | None = None
    Score: str | None = None # float string
    steps: int | None = None
    prompt: str | None = None
    sampler: str | None = None
    Eta_DDIM: str | None = Field(default=None, alias="Eta DDIM") # float string
    cfgScale: float | None = None
    resources: List[Any] | None = None
    Model_hash: str | None = Field(default=None, alias="Model hash") # short hash string
    Hires_upscale: str | None = Field(default=None, alias="Hires upscale") # float str
    Hires_upscaler: str | None = Field(default=None, alias="Hires upscaler") # hires upscaler name
    negativePrompt: str | None = None
    Denoising_strength: str | None = Field(default=None, alias="Denoising strength") # float string

class Response_Models_modelVersions_Image(BaseModel):
    url: str 	# The url for the image
    nsfwLevel: int 	# Whether or not the image is NSFW (note: if the model is NSFW, treat all images on the model as NSFW)
    width: int 	# The original width of the image
    height: int 	# The original height of the image
    hash: str 	#The blurhash of the image
    meta: Response_Models_modelVersions_Images_Meta | None = None	# The generation params of the image

class Response_Models_modelVersions_Stats(BaseModel):
    downloadCount: int # The number of downloads the model has
    ratingCount: int # The number of ratings the model has
    rating: float # The average rating of the model

class Response_Models_modelVersions_Model(BaseModel):
    name: str # The name of the model
    type: Response_Models_Type
    nsfw: bool # Whether the model is NSFW or not
    poi: bool # Whether the model is a Point of Interest model

class Response_Models_modelVersion(BaseModel):
    id: int	# The identifier for the model version
    modelId: int | None = None # The model id
    baseModel: str # The base model of the model
    name: str # The name of the model version
    earlyAccessEndsAt: str | None = None # (ISO 8601) The date in which the early access ends
    earlyAccessConfig: Dict[str, Any] | None = None # The early access configuration
    uploadType: str | None = None # The upload type of the model version
    description: str | None = None # The description of the model version (usually a changelog)
    createdAt: str | None = None # (ISO 8601) The date in which the version was created
    updatedAt: str | None = None # (ISO 8601) The date in which the version was updated
    status: str | None = None # The status of the model version
    publishedAt: str # (ISO 8601) The date in which the version was published, Only available for the model version query endpoint
    downloadUrl: str 	# The download url to get the model file for this specific version
    trainedWords: List[str] | None = None 	# The words used to trigger the model
    files: List[Response_Models_modelVersions_File]
    images: List[Response_Models_modelVersions_Image] | None = None
    stats: Response_Models_modelVersions_Stats

class Response_Models_Metadata(BaseModel):
    totalItems: int | None = None 	# The total number of items available
    currentPage: int | None = None 	# The the current page you are at
    pageSize: int | None = None 	# The the size of the batch
    totalPages: int | None = None 	# The total number of pages
    nextPage: str | None = None	# The url to get the next batch of items
    prevPage: str | None = None	# The url to get the previous batch of items

class Response_Model(BaseModel):
    id: int 	# The identifier for the model
    name: str 	# The name of the model
    description: str 	# The description of the model (HTML)
    type: Response_Models_Type | None = None # The model type
    nsfw: bool # Whether the model is NSFW or not
    tags: List[str] # The tags associated with the model
    mode: Response_Models_Mode | None = None 	# The mode in which the model is currently on. If Archived, files field will be empty. If TakenDown, images field will be empty
    creator: Response_Models_Creator | None = None 	# The creator of the model
    stats: Response_Models_Stats
    modelVersions: List[Response_Models_modelVersion]

class Response_Models(BaseModel):
    items: List[Response_Model]
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

LimitInt = Annotated[int, Field(strict=True, ge=1, le=100)]
Limit = Annotated[List[LimitInt], Len(1, 1)]
class Models_API_Opts(BaseModel):
    limit: 	None | Limit = None 	# The number of results to be returned per page. This can be a number between 1 and 100. By default, each page will return 100 results
    page: 	None | Annotated[List[StrictInt], Len(1,1)] = None 	# The page from which to start fetching models
    query: 	None | Annotated[List[str], Len(1,1)] = None 	# Search query to filter models by name
    tag: 	None | Annotated[List[str], Len(1,1)] = None 	# Search query to filter models by tag
    username: 	Optional[str] = None 	# Search query to filter models by user
    types: List[Response_Models_Type] | None = None 	# The type of model you want to filter with. If none is specified, it will return all types
    sort: 	None | Annotated[List[Sort], Len(1,1)] = None 	# The order in which you wish to sort the results
    period: None | Annotated[List[Period], Len(1,1)] = None 	# The time frame in which the models will be sorted
    # rating: 	Optional[int] 	# (Deprecated) The rating you wish to filter the models with. If none is specified, it will return models with any rating
    favorites: None | Annotated[List[StrictBool], Len(1,1)] = None 	# (AUTHED) Filter to favorites of the authenticated user (this requires an API token or session cookie)
    hidden: None | Annotated[List[StrictBool], Len(1,1)] = None 	# (AUTHED) Filter to hidden models of the authenticated user (this requires an API token or session cookie)
    primaryFileOnly: None | Annotated[List[StrictBool], Len(1,1)] = None 	# Only include the primary file for each model (This will use your preferred format options if you use an API token or session cookie)
    allowNoCredit: None | Annotated[List[StrictBool], Len(1,1)] = None 	# Filter to models that require or don't require crediting the creator
    allowDerivatives: None | Annotated[List[StrictBool], Len(1,1)] = None 	# Filter to models that allow or don't allow creating derivatives
    allowDifferentLicenses: None | Annotated[List[StrictBool], Len(1,1)] = None # Filter to models that allow or don't allow derivatives to have a different license
    allowCommercialUse: List[AllowCommercialUse] | None = None 	# Filter to models based on their commercial permissions
    nsfw: None | Annotated[List[StrictBool], Len(1,1)] = None # If false, will return safer images and hide models that don't have safe images
    supportsGeneration: None | Annotated[List[StrictBool], Len(1,1)] = None 	# If true, will return models that support generation