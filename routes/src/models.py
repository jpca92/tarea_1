from db import db
from datetime import datetime
import uuid

class Route(db.Model):
    """Modelo para la tabla de trayectos (routes)."""
    __tablename__ = 'routes'  # 🔹 Nombre de la tabla en minúsculas para PostgreSQL

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    flightId = db.Column(db.String, unique=True, nullable=False)
    sourceAirportCode = db.Column(db.String, nullable=False)
    sourceCountry = db.Column(db.String, nullable=False)
    destinyAirportCode = db.Column(db.String, nullable=False)
    destinyCountry = db.Column(db.String, nullable=False)
    bagCost = db.Column(db.Integer, nullable=False)
    plannedStartDate = db.Column(db.DateTime, nullable=False)
    plannedEndDate = db.Column(db.DateTime, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Devuelve una representación legible del objeto Route."""
        return f"<Route flightId={self.flightId} source={self.sourceAirportCode} -> destiny={self.destinyAirportCode}>"

    def to_json(self):
        """Convierte el objeto en un diccionario serializable en JSON."""
        return {
            "id": self.id,
            "flightId": self.flightId,
            "sourceAirportCode": self.sourceAirportCode,
            "sourceCountry": self.sourceCountry,
            "destinyAirportCode": self.destinyAirportCode,
            "destinyCountry": self.destinyCountry,
            "bagCost": self.bagCost,
            "plannedStartDate": self.plannedStartDate.isoformat(),
            "plannedEndDate": self.plannedEndDate.isoformat(),
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }

