from db import db
from datetime import datetime
import uuid

class Post(db.Model):
    """Modelo para la tabla de publicaciones."""
    __tablename__ = 'posts'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    route_id = db.Column(db.UUID, nullable=False)
    user_id = db.Column(db.UUID, nullable=False)
    expire_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.id}>"
