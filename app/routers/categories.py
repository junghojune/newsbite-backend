from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.deps import get_db
from ..models import Category


router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return {"success": True, "data": [c.name for c in categories]}

