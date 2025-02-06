from flask import Blueprint
from routes.users import users_bp

def register_routes(app):
    """Registra todas las rutas del microservicio."""
    app.register_blueprint(users_bp)
