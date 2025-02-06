from flask import Blueprint
from .posts import posts_bp

def register_routes(app):
    """Registra todas las rutas del microservicio."""
    app.register_blueprint(posts_bp)
