from typing import List
from pydantic import BaseModel
import enum
from .models import Response_Models_Type

class Response_ModelByVersionId_Model_Mode(enum.Enum):
    Archived = "Archived"
    TakenDown = "TakenDown"

# class Response_ModelByVersionId_Model_Type(enum.Enum):
#     Checkpoint = "Checkpoint"
#     TextualInversion = "TextualInversion"
#     Hypernetwork = "Hypernetwork"
#     AestheticGradient = "AestheticGradient"
#     LORA = "LORA"
#     Controlnet = "Controlnet"
#     Poses = "Poses"

class Response_ModelByVersionId_Model(BaseModel):
    name: 	str 	# The name of the model
    type: 	Response_Models_Type 	# The model type
    nsfw: 	bool 	# Whether the model is NSFW or not
    poi: 	bool 	# Whether the model is of a person of interest or not
    mode: 	Response_ModelByVersionId_Model_Mode | None = None # The mode in which the model is currently on. If Archived, files field will be empty. If TakenDown, images field will be empty

class Response_ModelByVersionId_Files_Metadata_Fp(enum.Enum):
    fp16 = "fp16"
    fp32 = "fp32"

class Response_ModelByVersionId_Files_Metadata_Size(enum.Enum):
    full = "full"
    pruned = "pruned"
    
class Response_ModelByVersionId_Files_Metadata_Format(enum.Enum):
    SafeTensor = "SafeTensor"
    PickleTensor = "PickleTensor"
    Other = "Other"

class Response_ModelByVersionId_Files_Metadata(BaseModel):
    fp: Response_ModelByVersionId_Files_Metadata_Fp | None 	# The specified floating point for the file
    size: Response_ModelByVersionId_Files_Metadata_Size | None 	# The specified model size for the file
    format: Response_ModelByVersionId_Files_Metadata_Format | None 	# The specified model format for the file

class Response_ModelByVersionId_Files(BaseModel):
    sizeKb: 	int 	# The size of the model file
    pickleScanResult: 	str 	# Status of the pickle scan ('Pending', 'Success', 'Danger', 'Error')
    virusScanResult: 	str 	# Status of the virus scan ('Pending', 'Success', 'Danger', 'Error')
    scannedAt: 	str | None 	# (ISO 8601) The date in which the file was scanned
    metadata: Response_ModelByVersionId_Files_Metadata
    

from .models import Response_Models_modelVersions_Stats, Response_Models_modelVersions_Image, Response_Models_modelVersions_File

class Response_ModelByVersionId(BaseModel):
    id: 	int 	# The identifier for the model version
    name: 	str 	# The name of the model version
    description: 	str 	# The description of the model version (usually a changelog)
    baseModel: Response_ModelByVersionId_Model
    modelId: 	int 	# The identifier for the model
    createdAt: 	str 	# (ISO 8601) The date in which the version was created
    updatedAt: 	str 	# (ISO 8601) The date in which the version was updated
    downloadUrl: 	str 	# The download url to get the model file for this specific version
    trainedWords: 	List[str] 	# The words used to trigger the model
    files: Response_Models_modelVersions_File
    stats: Response_Models_modelVersions_Stats
    images: Response_Models_modelVersions_Image
    