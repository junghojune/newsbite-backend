from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.deps import get_db
from ..models import Article, Summary, Category, ArticleCategory
from ..schemas.news import PaginatedNews, NewsItem


router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/today", response_model=PaginatedNews)
def get_today_news(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_news_by_date(date.today(), page=page, size=size, db=db)


@router.get("", response_model=PaginatedNews)
def get_news(
    date_str: Optional[str] = Query(None, alias="date"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    target_date: Optional[date] = None
    if date_str:
        target_date = date.fromisoformat(date_str)
    else:
        target_date = date.today()
    return list_news_by_date(target_date, page=page, size=size, db=db)


def list_news_by_date(target_date: date, page: int, size: int, db: Session) -> PaginatedNews:
    start = (page - 1) * size
    end = start + size

    # 간단 구현: published_at의 날짜가 target_date인 기사만 필터
    q = db.query(Article).filter(Article.published_at != None)  # noqa: E711
    q = q.filter(Article.published_at >= f"{target_date.isoformat()} 00:00:00")
    q = q.filter(Article.published_at <= f"{target_date.isoformat()} 23:59:59")
    q = q.order_by(Article.published_at.desc())

    total = q.count()
    articles = q.offset(start).limit(size).all()

    # 요약/카테고리 1건만 매핑(최신 요약 우선)
    items: list[NewsItem] = []
    for a in articles:
        s: Optional[Summary] = (
            db.query(Summary).filter(Summary.article_id == a.id).order_by(Summary.created_at.desc()).first()
        )
        category_name: Optional[str] = None
        ac = (
            db.query(ArticleCategory)
            .filter(ArticleCategory.article_id == a.id)
            .order_by(ArticleCategory.id.desc())
            .first()
        )
        if ac:
            cat = db.query(Category).filter(Category.id == ac.category_id).first()
            if cat:
                category_name = cat.name

        items.append(
            NewsItem(
                id=a.id,
                title=a.title,
                summary=s.summary if s else None,
                category=category_name,
                url=a.url,
                published_at=a.published_at,
            )
        )

    return PaginatedNews(items=items, page=page, size=size, total=total)

