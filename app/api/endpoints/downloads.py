# Routes for handling download-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import download as crud_download
from app.schemas.download import DownloadBase, DownloadOut

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


@router.post("/", response_model=DownloadOut)
def create_download(download_data: DownloadBase, db: Session = Depends(get_db)):
    """Endpoint to create a new download."""
    download = crud_download.add_download(db, download_data)
    return download


@router.put("/{download_id}", response_model=DownloadOut)
def update_download(download_id: int, download_data: DownloadBase, db: Session = Depends(get_db)):
    """Endpoint to update an existing download."""
    existing_download = crud_download.get_download_by_id(db, download_id)
    if existing_download is None:
        raise HTTPException(status_code=404, detail="Download not found")
    updated_download = crud_download.edit_download(
        db, download_id, download_data)
    return updated_download


@router.delete("/{download_id}")
def delete_download(download_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete a specific download by its ID."""
    existing_download = crud_download.get_download_by_id(db, download_id)
    if existing_download is None:
        raise HTTPException(status_code=404, detail="Download not found")
    crud_download.remove_download(db, download_id)
    return {"msg": "Download deleted successfully"}
