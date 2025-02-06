from flask import Blueprint, request, jsonify
from db import db
from models import Route
from datetime import datetime
import uuid

routes_bp = Blueprint('routes', __name__)

### CREAR TRAYECTO ###
@routes_bp.route('/routes', methods=['POST'])
def create_route():
    data = request.get_json()
    token_user_id = request.headers.get("Authorization")

    # Validar si hay token
    if not token_user_id:
        return jsonify({"msg": "No hay token en la solicitud"}), 403

    # Validar si faltan campos en la solicitud
    required_fields = ["flightId", "sourceAirportCode", "sourceCountry",
                       "destinyAirportCode", "destinyCountry", "bagCost",
                       "plannedStartDate", "plannedEndDate"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Parámetros inválidos"}), 400

    # Validar que `flightId` no exista
    existing_route = Route.query.filter_by(flightId=data['flightId']).first()
    if existing_route:
        return jsonify({"msg": "El flightId ya existe"}), 412

    # Validar fechas
    try:
        planned_start_date = datetime.fromisoformat(data['plannedStartDate'])
        planned_end_date = datetime.fromisoformat(data['plannedEndDate'])
        if planned_start_date >= planned_end_date or planned_start_date < datetime.utcnow():
            return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412
    except ValueError:
        return jsonify({"msg": "Formato de fecha inválido"}), 400

    # Crear el trayecto
    route = Route(
        id=str(uuid.uuid4()),
        flightId=data["flightId"],
        sourceAirportCode=data["sourceAirportCode"],
        sourceCountry=data["sourceCountry"],
        destinyAirportCode=data["destinyAirportCode"],
        destinyCountry=data["destinyCountry"],
        bagCost=data["bagCost"],
        plannedStartDate=planned_start_date,
        plannedEndDate=planned_end_date,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )

    # Guardar en la base de datos
    db.session.add(route)
    db.session.commit()

    return jsonify({"id": route.id, "createdAt": route.createdAt.isoformat()}), 201


### OBTENER TRAYECTOS (CON FILTRO OPCIONAL) ###
@routes_bp.route('/routes', methods=['GET'])
def get_routes():
    token_user_id = request.headers.get("Authorization")
    if not token_user_id:
        return jsonify({"msg": "No hay token en la solicitud"}), 403

    flight_id = request.args.get("flight")
    query = Route.query
    if flight_id:
        query = query.filter_by(flightId=flight_id)

    routes = query.all()
    return jsonify([route.to_json() for route in routes]), 200


### CONSULTAR UN TRAYECTO POR ID ###
@routes_bp.route('/routes/<string:route_id>', methods=['GET'])
def get_route_by_id(route_id):
    token_user_id = request.headers.get("Authorization")
    if not token_user_id:
        return jsonify({"msg": "No hay token en la solicitud"}), 403

    # Validar que el ID sea un UUID válido
    try:
        uuid.UUID(route_id)
    except ValueError:
        return jsonify({"msg": "El id no es un valor string con formato uuid"}), 400

    route = Route.query.get(route_id)
    if not route:
        return jsonify({"msg": "El trayecto con ese id no existe"}), 404

    return jsonify(route.to_json()), 200


### ELIMINAR TRAYECTO ###
@routes_bp.route('/routes/<string:route_id>', methods=['DELETE'])
def delete_route(route_id):
    token_user_id = request.headers.get("Authorization")
    if not token_user_id:
        return jsonify({"msg": "No hay token en la solicitud"}), 403

    # Validar que el ID sea un UUID válido
    try:
        uuid.UUID(route_id)
    except ValueError:
        return jsonify({"msg": "El id no es un valor string con formato uuid"}), 400

    route = Route.query.get(route_id)
    if not route:
        return jsonify({"msg": "El trayecto con ese id no existe"}), 404

    db.session.delete(route)
    db.session.commit()
    
    return jsonify({"msg": "El trayecto fue eliminado"}), 200


### HEALTH CHECK ###
@routes_bp.route('/routes/ping', methods=['GET'])
def health_check():
    return "pong", 200


### RESETEAR BASE DE DATOS ###
@routes_bp.route('/routes/reset', methods=['POST'])
def reset_database():
    db.session.query(Route).delete()
    db.session.commit()
    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
