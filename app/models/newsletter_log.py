from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.sql import func
from ..db.base import Base


class NewsletterLog(Base):
    __tablename__ = "newsletter_logs"

    id = Column(Integer, primary_key=True)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    payload = Column(Text, nullable=True)  # 포함된 기사 목록/메타 JSON 직렬화용

