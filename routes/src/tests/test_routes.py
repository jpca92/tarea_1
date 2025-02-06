import pytest
import uuid
from datetime import datetime, timedelta
from flask import Flask
from src.db import db
from src.models import Route
from src.routes.routes import routes_bp

@pytest.fixture
def app():
    """ Configuración de la aplicación en modo prueba """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Base de datos en memoria para pruebas
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)
    return app

@pytest.fixture
def client(app):
    """ Cliente de pruebas para realizar peticiones """
    return app.test_client()


### 🧪 TEST: Health Check ###
def test_health_check(client):
    response = client.get("/routes/ping")
    assert response.status_code == 200
    assert response.data.decode() == "pong"


### 🧪 TEST: Crear un trayecto ###
def test_create_route(client):
    route_data = {
        "flightId": "AA123",
        "sourceAirportCode": "BOG",
        "sourceCountry": "Colombia",
        "destinyAirportCode": "JFK",
        "destinyCountry": "EEUU",
        "bagCost": 50,
        "plannedStartDate": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "plannedEndDate": (datetime.utcnow() + timedelta(days=3)).isoformat()
    }
    headers = {"Authorization": "Bearer test_token"}
    response = client.post("/routes", json=route_data, headers=headers)

    assert response.status_code == 201
    json_data = response.get_json()
    assert "id" in json_data
    assert "createdAt" in json_data


### 🧪 TEST: Crear un trayecto sin token ###
def test_create_route_no_token(client):
    route_data = {
        "flightId": "BB456",
        "sourceAirportCode": "MEX",
        "sourceCountry": "México",
        "destinyAirportCode": "CDG",
        "destinyCountry": "Francia",
        "bagCost": 70,
        "plannedStartDate": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "plannedEndDate": (datetime.utcnow() + timedelta(days=3)).isoformat()
    }
    response = client.post("/routes", json=route_data)

    assert response.status_code == 403
    assert response.get_json()["msg"] == "No hay token en la solicitud"


### 🧪 TEST: Obtener lista de trayectos ###
def test_get_routes(client):
    headers = {"Authorization": "Bearer test_token"}
    response = client.get("/routes", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


### 🧪 TEST: Consultar un trayecto por ID ###
def test_get_route_by_id(client):
    headers = {"Authorization": "Bearer test_token"}

    # Crear un trayecto de prueba
    route = Route(
        id=str(uuid.uuid4()),
        flightId="CC789",
        sourceAirportCode="LIM",
        sourceCountry="Perú",
        destinyAirportCode="MAD",
        destinyCountry="España",
        bagCost=90,
        plannedStartDate=datetime.utcnow() + timedelta(days=2),
        plannedEndDate=datetime.utcnow() + timedelta(days=3),
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    db.session.add(route)
    db.session.commit()

    # Obtener la ruta recién creada
    response = client.get(f"/routes/{route.id}", headers=headers)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["id"] == route.id


### 🧪 TEST: Intentar obtener un trayecto con ID inválido ###
def test_get_route_invalid_id(client):
    headers = {"Authorization": "Bearer test_token"}
    response = client.get("/routes/invalid-id", headers=headers)

    assert response.status_code == 400
    assert response.get_json()["msg"] == "El id no es un valor string con formato uuid"


### 🧪 TEST: Eliminar un trayecto ###
def test_delete_route(client):
    headers = {"Authorization": "Bearer test_token"}

    # Crear un trayecto de prueba
    route = Route(
        id=str(uuid.uuid4()),
        flightId="DD999",
        sourceAirportCode="SCL",
        sourceCountry="Chile",
        destinyAirportCode="GRU",
        destinyCountry="Brasil",
        bagCost=100,
        plannedStartDate=datetime.utcnow() + timedelta(days=2),
        plannedEndDate=datetime.utcnow() + timedelta(days=3),
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    db.session.add(route)
    db.session.commit()

    # Eliminar la ruta
    response = client.delete(f"/routes/{route.id}", headers=headers)

    assert response.status_code == 200
    assert response.get_json()["msg"] == "El trayecto fue eliminado"


### 🧪 TEST: Intentar eliminar un trayecto con ID que no existe ###
def test_delete_nonexistent_route(client):
    headers = {"Authorization": "Bearer test_token"}
    nonexistent_id = str(uuid.uuid4())

    response = client.delete(f"/routes/{nonexistent_id}", headers=headers)

    assert response.status_code == 404
    assert response.get_json()["msg"] == "El trayecto con ese id no existe"


### 🧪 TEST: Resetear la base de datos ###
def test_reset_database(client):
    headers = {"Authorization": "Bearer test_token"}
    
    # Crear trayectos de prueba
    for i in range(3):
        route = Route(
            id=str(uuid.uuid4()),
            flightId=f"TEST{i}",
            sourceAirportCode="SFO",
            sourceCountry="USA",
            destinyAirportCode="LHR",
            destinyCountry="UK",
            bagCost=150,
            plannedStartDate=datetime.utcnow() + timedelta(days=2),
            plannedEndDate=datetime.utcnow() + timedelta(days=3),
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(route)
    
    db.session.commit()

    # Verificar que hay datos antes del reset
    assert Route.query.count() > 0

    # Resetear la base de datos
    response = client.post("/routes/reset", headers=headers)

    assert response.status_code == 200
    assert response.get_json()["msg"] == "Todos los datos fueron eliminados"

    # Verificar que la base de datos está vacía
    assert Route.query.count() == 0
