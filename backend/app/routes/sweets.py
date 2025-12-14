from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Sweet
from ..deps import get_current_user, admin_only
from pydantic import BaseModel



router = APIRouter()

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_sweet(
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    new_sweet = Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet



@router.get("/")
def list_sweets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)  
):
    return db.query(Sweet).all()

@router.post("/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int, db: Session = Depends(get_db)):
    sweet = db.query(Sweet).get(sweet_id)
    if not sweet or sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    sweet.quantity -= 1
    db.commit()
    return sweet

@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    sweet = db.query(Sweet).get(sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(sweet)
    db.commit()
    return {"message": "Sweet deleted"}

@router.post("/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sweet = db.query(Sweet).get(sweet_id)
    if not sweet or sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    sweet.quantity -= 1
    db.commit()
    return sweet

@router.get("/search")
def search_sweets(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))

    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)

    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    return query.all()
