from datetime import datetime, timezone
import uuid
from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base() 
class Model(Base):
    """Modelo para la tabla de usuarios."""
    __abstract__=True

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
        self.updated_at = datetime.now(timezone.utc).isoformat(timespec='seconds')

                           
