from flask import Blueprint
from routes.routes import routes_bp

def register_routes(app):
    """Registra todas las rutas del microservicio."""
    app.register_blueprint(routes_bp)
