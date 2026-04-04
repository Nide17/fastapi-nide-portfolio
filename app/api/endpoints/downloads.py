# Routes for handling download-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import download as crud_download
from app.schemas.download import DownloadOut

router = APIRouter()

@router.get("/", response_model=list[DownloadOut])
def read_downloads(db: Session = Depends(get_db)):
    """Endpoint to fetch all downloads."""
    downloads = crud_download.get_all_downloads(db)
    return downloads

@router.get("/{download_id}", response_model=DownloadOut)
def read_download(download_id: int, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific download by its ID."""
    download = crud_download.get_download_by_id(db, download_id)
    if download is None:
        raise HTTPException(status_code=404, detail="Download not found")
    return download
