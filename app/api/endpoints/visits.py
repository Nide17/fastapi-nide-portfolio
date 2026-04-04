# Routes for handling visit-related API endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import visit as crud_visit
from app.schemas.visit import VisitBase, VisitOut

router = APIRouter()

@router.get("/", response_model=list[VisitOut])
def read_visits(db: Session = Depends(get_db)):
    """Endpoint to fetch all visits."""
    visits = crud_visit.get_all_visits(db)
    return visits

@router.get("/{visit_id}", response_model=VisitOut)
def read_visit(visit_id: int, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific visit by its ID."""
    visit = crud_visit.get_visit_by_id(db, visit_id)
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@router.post("/", response_model=VisitOut)
def create_visit(visit_data: VisitBase, db: Session = Depends(get_db)):
    """Endpoint to create a new visit."""
    visit = crud_visit.add_visit(db, visit_data)
    return visit

@router.put("/{visit_id}", response_model=VisitOut)
def update_visit(visit_id: int, visit_data: VisitBase, db: Session = Depends(get_db)):
    """Endpoint to update an existing visit."""
    visit = crud_visit.edit_visit(db, visit_id, visit_data)
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit
