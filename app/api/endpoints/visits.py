# Routes for handling visit-related API endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core import auth
from app.crud import visit as crud_visit
from app.schemas.visit import VisitBase, VisitOut

router = APIRouter()


@router.get("/", response_model=list[VisitOut])
def read_visits(db: Session = Depends(get_db)):
    """Endpoint to fetch all visits."""
    try:
        visits = crud_visit.get_all_visits(db)
        return visits
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch visits. Check logs.")


@router.get("/{visit_id}", response_model=VisitOut)
def read_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    """Endpoint to fetch a specific visit by its ID."""
    visit = crud_visit.get_visit_by_id(db, visit_id)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.post("/", response_model=VisitOut)
def create_visit(visit_data: VisitBase, db: Session = Depends(get_db)):
    """Endpoint to create a new visit."""
    try:
        visit = crud_visit.add_visit(db, visit_data)
        return visit
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create visit. Invalid data or DB issue.")


@router.put("/{visit_id}", response_model=VisitOut)
def update_visit(
    visit_id: int,
    visit_data: VisitBase,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    """Endpoint to update an existing visit."""
    existing_visit = crud_visit.get_visit_by_id(db, visit_id)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if existing_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    visit = crud_visit.edit_visit(db, visit_id, visit_data)
    return visit


@router.delete("/{visit_id}")
def delete_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    """Endpoint to delete a specific visit by its ID."""
    existing_visit = crud_visit.get_visit_by_id(db, visit_id)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if existing_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    crud_visit.remove_visit(db, visit_id)
    return {"msg": "Visit deleted successfully"}
