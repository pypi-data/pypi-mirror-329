import enum
from _typeshed import Incomplete
from pydantic import BaseModel, StrictInt as StrictInt
from typing import Annotated

class NsfwLevel(enum.Enum):
    None_ = 'None'
    Soft = 'Soft'
    Mature = 'Mature'
    X = 'X'

class Sort(enum.Enum):
    Most_Reactions = 'Most Reactions'
    Most_Comments = 'Most Comments'
    Newest = 'Newest'

class Period(enum.Enum):
    AllTime = 'AllTime'
    Day = 'Day'
    Week = 'Week'
    Month = 'Month'
    Year = 'Year'

class Response_Images_Stats(BaseModel):
    cryCount: int
    laughCount: int
    likeCount: int
    heartCount: int
    commentCount: int

class Response_Images_Meta_CivitaiResources_Type(enum.Enum):
    checkpoint = 'checkpoint'
    lora = 'lora'

class Response_Images_Meta_Resources(BaseModel):
    hash: str
    name: str
    type: Response_Images_Meta_CivitaiResources_Type
    weight: float | None

class Response_Images_Meta_CivitaiResources(BaseModel):
    type: Response_Images_Meta_CivitaiResources_Type
    weight: float | None
    modelVersionId: int
    modelVersionName: str | None

class Response_Images_Meta(BaseModel):
    Size: str
    seed: int
    vaes: str | None
    comfy: str | None
    Model: str
    steps: int
    prompt: str
    sampler: str
    Version: str
    cfgScale: int
    clipSkip: str
    resources: list[Response_Images_Meta_Resources]
    civitaiResources: list[Response_Images_Meta_CivitaiResources]
    Hires_upscale: str | None
    Hires_upscaler: str | None
    negativePrompt: str
    Denoising_strength: str | None
    ADetailer_model: str | None
    ADetailer_version: str | None
    ADetailer_mask_blur: str | None
    ADetailer_confidence: str | None
    ADetailer_dilate_erode: str | None
    ADetailer_inpaint_padding: str | None
    ADetailer_denoising_strength: str | None
    ADetailer_inpaint_only_masked: str | None

class Response_Images_Metadata(BaseModel):
    nextCursor: int | str | None
    currentPage: int | None
    pageSize: int | None
    nextPage: str | None

class Response_Images_Item(BaseModel):
    id: int
    url: str
    hash: str
    width: int
    height: int
    nsfw: bool
    nsfwLevel: NsfwLevel
    createdAt: str
    postId: int
    stats: Response_Images_Stats
    meta: dict | None
    username: str | None
    baseModel: str | None

class Response_Images(BaseModel):
    items: list[Response_Images_Item]
    metadata: Response_Images_Metadata

LimitInt: Incomplete
Limit: Incomplete

class Images_API_Opts(BaseModel):
    limit: None | Limit
    postId: None | Annotated[list[StrictInt], None]
    modelId: None | Annotated[list[StrictInt], None]
    modelVersionId: None | Annotated[list[StrictInt], None]
    username: None | Annotated[list[str], None]
    nsfw: None | list[NsfwLevel]
    sort: None | Annotated[list[Sort], None]
    period: None | Annotated[list[Period], None]
    page: None | StrictInt
