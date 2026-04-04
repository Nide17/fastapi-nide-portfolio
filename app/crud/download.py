# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.download import Download

def get_all_downloads(db: Session):
    """Fetches all downloads from the database."""
    return db.query(Download).all()

def get_download_by_id(db: Session, download_id: int):
    """Fetches a single download by its ID."""
    return db.query(Download).filter(Download.id == download_id).first()
