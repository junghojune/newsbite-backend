from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsItem(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    category: Optional[str] = None
    url: str
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedNews(BaseModel):
    items: list[NewsItem]
    page: int
    size: int
    total: int

