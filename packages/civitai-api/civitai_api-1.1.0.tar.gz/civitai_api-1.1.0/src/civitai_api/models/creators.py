from typing import Annotated, List
from annotated_types import Len
from pydantic import BaseModel, Field, StrictInt

class Response_Creaters_Item(BaseModel):
    username: str
    modelCount: int | None = None
    link: str

class Response_Creaters_Metadata(BaseModel):
    totalItems: int
    currentPage: int
    pageSize: int
    totalPages: int
    nextPage: str

class Response_Creaters(BaseModel):
    items: List[Response_Creaters_Item]
    metadata: Response_Creaters_Metadata


LimitInt = Annotated[int, Field(strict=True, ge=1, le=200)]
Limit = Annotated[List[LimitInt], Len(1, 1)]
class Creators_API_Opts(BaseModel):
    limit: None | Limit = None # The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 20 results. If set to 0, it'll return all the creators
    page: None | Annotated[List[StrictInt], Len(1,1)] = None  # The page from which to start fetching creators
    query: None | Annotated[List[str], Len(1,1)] = None # Search query to filter creators by username