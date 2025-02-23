from _typeshed import Incomplete
from pydantic import BaseModel, StrictInt as StrictInt
from typing import Annotated

class Response_Creaters_Item(BaseModel):
    username: str
    modelCount: int | None
    link: str

class Response_Creaters_Metadata(BaseModel):
    totalItems: int
    currentPage: int
    pageSize: int
    totalPages: int
    nextPage: str

class Response_Creaters(BaseModel):
    items: list[Response_Creaters_Item]
    metadata: Response_Creaters_Metadata

LimitInt: Incomplete
Limit: Incomplete

class Creators_API_Opts(BaseModel):
    limit: None | Limit
    page: None | Annotated[list[StrictInt], None]
    query: None | Annotated[list[str], None]
