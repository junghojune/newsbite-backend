from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from ..db.base import Base


class ArticleCategory(Base):
    __tablename__ = "article_categories"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("article_id", "category_id", name="uq_article_category"),
    )

