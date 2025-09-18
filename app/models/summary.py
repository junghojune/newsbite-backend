from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    category = Column(String(64), nullable=True)
    model = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    article = relationship("Article", backref="summaries")

