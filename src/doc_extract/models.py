from pydantic import BaseModel


class PageInfo(BaseModel):
    page: int
    chars: int
    images: int
    page_type: str


class ExtractionResult(BaseModel):
    request_id: str
    pages: int
    valid: bool
    data: dict
    errors: list[str]
    retry_count: int
    pages_succeeded: list[int]
    pages_failed: list[int]
