from typing import List
from pydantic import BaseModel

class Response_Tags_Metadata(BaseModel):
    totalItems: int # The total number of items available
    currentPage: int # The the current page you are at
    pageSize: int # The the size of the batch
    totalPages: int # The total number of pages
    nextPage: str | None # The url to get the next batch of items
    prevPage: str | None # The url to get the previous batch of items

class Response_Tags_Items(BaseModel):
    name: str # The name of the tag
    modelCount: int # The amount of models linked to this tag
    link: str # Url to get all models from this tag

class Response_Tags(BaseModel):
    items: List[Response_Tags_Items]
    metadata: Response_Tags_Metadata
