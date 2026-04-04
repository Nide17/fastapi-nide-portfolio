# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.download import Download


def get_all_downloads(db: Session):
    """Fetches all downloads from the database."""
    return db.query(Download).all()


def get_download_by_id(db: Session, download_id: int):
    """Fetches a single download by its ID."""
    return db.query(Download).filter(Download.id == download_id).first()


def add_download(db: Session, download_data):
    """Creates a new download in the database."""
    new_download = Download(**download_data.model_dump())
    db.add(new_download)
    db.commit()
    db.refresh(new_download)
    return new_download


def edit_download(db: Session, download_id: int, download_data):
    """Updates an existing download in the database."""
    db.query(Download).filter(Download.id == download_id).update(download_data.model_dump())
    db.commit()
    return db.query(Download).filter(Download.id == download_id).first()


def remove_download(db: Session, download_id: int):
    """Deletes a download from the database."""
    db.query(Download).filter(Download.id == download_id).delete()
    db.commit()
