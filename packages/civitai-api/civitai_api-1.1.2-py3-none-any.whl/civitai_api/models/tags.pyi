from pydantic import BaseModel

class Response_Tags_Metadata(BaseModel):
    totalItems: int
    currentPage: int
    pageSize: int
    totalPages: int
    nextPage: str | None
    prevPage: str | None

class Response_Tags_Items(BaseModel):
    name: str
    modelCount: int
    link: str

class Response_Tags(BaseModel):
    items: list[Response_Tags_Items]
    metadata: Response_Tags_Metadata
