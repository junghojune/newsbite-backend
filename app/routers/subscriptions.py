from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..db.deps import get_db
from ..models import Subscription
from ..core.config import settings
from ..utils.tokens import generate_token, verify_token


router = APIRouter(prefix="/api", tags=["subscription"])


class SubscribeBody(BaseModel):
    email: EmailStr


@router.post("/subscribe")
def subscribe(body: SubscribeBody, db: Session = Depends(get_db)):
    email = body.email.lower()
    sub = db.query(Subscription).filter(Subscription.email == email).first()
    if sub and sub.is_active:
        return {"success": True}
    if not sub:
        sub = Subscription(email=email, is_active=False)
        db.add(sub)
        db.commit()
        db.refresh(sub)

    token = generate_token(email=email, purpose="confirm", secret=settings.timezone)  # 임시로 timezone을 비밀키 대용
    # TODO: 실제 메일 발송 로직으로 대체
    return {"success": True, "data": {"confirm_token": token}}


@router.get("/subscribe/confirm")
def confirm(token: str, db: Session = Depends(get_db)):
    ok, email = verify_token(token, purpose="confirm", secret=settings.timezone)
    if not ok or not email:
        raise HTTPException(status_code=400, detail="invalid or expired token")
    sub = db.query(Subscription).filter(Subscription.email == email).first()
    if not sub:
        raise HTTPException(status_code=404, detail="subscription not found")
    if not sub.is_active:
        sub.is_active = True
        db.add(sub)
        db.commit()
    return {"success": True}


class UnsubscribeBody(BaseModel):
    email: EmailStr
    token: str | None = None


@router.post("/unsubscribe")
def unsubscribe(body: UnsubscribeBody, db: Session = Depends(get_db)):
    email = body.email.lower()
    sub = db.query(Subscription).filter(Subscription.email == email).first()
    if not sub:
        return {"success": True}
    sub.is_active = False
    db.add(sub)
    db.commit()
    return {"success": True}

