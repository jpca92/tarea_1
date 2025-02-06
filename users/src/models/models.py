from sqlalchemy import Column, DateTime, String
from db import db
from datetime import datetime
import uuid

from .model import Model

class User(Model):
    """Modelo para la tabla de usuarios."""
    __tablename__ = 'users'  # Especifica el nombre correcto de la tabla
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=True)
    dni = Column(String(20), nullable=True)
    full_name = Column(String(100), nullable=True)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, 
                       default='POR_VERIFICAR', 
                       check_constraint="status IN ('POR_VERIFICAR', 'NO_VERIFICADO', 'VERIFICADO')")
    expire_at = Column(DateTime, nullable=True)

    

    def __init__(self, username, password, email, dni, full_name, phone_number,salt, status ):
        # Para inicializar la instancia del modelo que estamos heredando
        Model.__init__(self)
        self.username = username
        self.password = password
        self.email = email
        self.dni = dni
        self.full_name = full_name
        self.phone_number = phone_number
        self.salt=salt,       
        self.status = status


    def __repr__(self):
        return f"<User {self.username}>"
