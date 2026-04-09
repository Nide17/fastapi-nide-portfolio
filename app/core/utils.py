from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session


def get_existing_ip(db: Session, ip: str, model):
    """Checks if an entry exists in the database based on IP within a 24h window.

    Kept simple and pure-ish: it accepts a Session and a SQLAlchemy model that
    must have `ip_address` and `created_at` columns.
    """

    window = datetime.now(timezone.utc) - timedelta(days=1)

    existing = db.query(model).filter(
        model.ip_address == ip,
        model.created_at >= window
    ).first()

    if existing:
        return existing
    return None
