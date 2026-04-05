from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session


def get_existing_ip(db: Session, ip: str, model):
    """Checks if an entry exists in the database based on IP."""

    window = datetime.now(timezone.utc) - timedelta(days=1)

    existing = db.query(model).filter(
        model.ip_address == ip,
        model.created_at >= window
    ).first()

    if existing:
        return existing
    return None
