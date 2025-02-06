import sys
import os
import pytest

# ruta = os.path.abspath(os.path.dirname(__file__) + "/../src")
# sys.path.insert(0, ruta)

# Agregar src al sys.path para que pytest pueda encontrar los módulos
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print("Ruta agregada a sys.path:", ruta)

from ..app import app, db

from users.src.models.models import User
from werkzeug.security import generate_password_hash
import bcrypt
import secrets
import datetime

@pytest.fixture
def client():
    """Fixture para configurar la base de datos en memoria y un cliente de pruebas"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()  # Crea las tablas en la BD de prueba
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()  # Limpia la base de datos después de cada prueba

# Test para crear usuario
def test_create_user(client):
    response = client.post("/users", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    assert "id" in response.json

# Test para evitar duplicación de usuario
def test_create_duplicate_user(client):
    with app.app_context():
        client.post("/users", json={
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com"
        })
        response = client.post("/users", json={
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com"
        })
    assert response.status_code == 412
    assert "error" in response.json

# Test para actualizar usuario
def test_update_user(client):
    with app.app_context():
        user = User(username="testuser", password="hashed", email="test@example.com", salt="somesalt", status="VERIFICADO")
        db.session.add(user)
        db.session.commit()
        
        response = client.patch(f"/users/{user.id}", json={"fullName": "New Name"})
    assert response.status_code == 200
    assert response.json["msg"] == "El usuario ha sido actualizado"

# Test de autenticación y generación de token
def test_generate_token(client):
    with app.app_context():
        salt = bcrypt.gensalt().decode()
        hashed_password = generate_password_hash("testpassword" + salt)
        user = User(username="testuser", password=hashed_password, email="test@example.com", salt=salt, status="VERIFICADO")
        db.session.add(user)
        db.session.commit()

        response = client.post("/users/auth", json={
            "username": "testuser",
            "password": "testpassword"
        })
    assert response.status_code == 200
    assert "token" in response.json

# Test para obtener la información del usuario autenticado
def test_get_user_info(client):
    with app.app_context():
        salt = bcrypt.gensalt().decode()
        hashed_password = generate_password_hash("testpassword" + salt)
        token = secrets.token_hex(32)
        expire_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        user = User(username="testuser", password=hashed_password, email="test@example.com", salt=salt, status="VERIFICADO", token=token, expire_at=expire_at)
        db.session.add(user)
        db.session.commit()
        
        response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json["username"] == "testuser"

# Test para verificar el ping del microservicio
def test_ping(client):
    response = client.get("/users/ping")
    assert response.status_code == 200
    assert response.json["message"] == "Users microservice is running"

# Test para resetear la base de datos
def test_reset_db(client):
    with app.app_context():
        user = User(username="testuser", password="hashed", email="test@example.com", salt="somesalt", status="VERIFICADO")
        db.session.add(user)
        db.session.commit()
        
        response = client.post("/users/reset")
    assert response.status_code == 200
    assert response.json["message"] == "Database reset successfully"
    with app.app_context():
        assert User.query.count() == 0  # Verifica que la base de datos se haya limpiado