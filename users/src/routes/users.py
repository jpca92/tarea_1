from flask import Blueprint, request, jsonify
from models.models import User
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import secrets
import datetime

users_bp = Blueprint('users', __name__)

# Endpoint para crear un usuario
@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    print("[*] Datos recibidos:", data)  # Imprime los datos en la consola

    required_fields = ["username", "password", "email"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "username, password, and email are required"}), 400

    # Verificar si el usuario ya existe
    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"error": "Username or email already exists"}), 412
    
 # Generar salt y cifrar contraseña
    salt = bcrypt.gensalt().decode()
    hashed_password = generate_password_hash(data['password'] + salt)
       
    # Crear usuario con contraseña encriptada
    new_user = User(
        username=data["username"],
        password=hashed_password,
        email=data["email"],
        dni=data.get("dni"), 
        full_name=data.get("fullName"), 
        phone_number=data.get("phoneNumber"), 
        salt=salt,
        status="VERIFICADO"
    )

    # Imprime el usuario antes de guardar
    print("[*] Creando usuario:", new_user, flush=True)  

    db.session.add(new_user)
    # db.session.flush()  # Esto fuerza la inserción antes del commit
    print("[✅] Usuario insertado con ID:", new_user.id, flush = True)
    db.session.commit()
    # Confirmación de guardado
    print("[✅] Usuario guardado con ID:", new_user.id, flush = True)
    print("------------")  
    print(new_user, flush = True)

    return jsonify({
        "id": new_user.id,
        "createdAt": new_user.created_at.isoformat() + "Z"
    }), 201

# Endpoint para actualizar un usuario
@users_bp.route('/users/<uuid:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()

    # Validar que haya al menos un campo en la petición
    if not any(key in data for key in ["fullName", "phoneNumber", "dni", "status"]):
        return jsonify({"error": "Debe proporcionar al menos un campo para actualizar"}), 400

    # Actualizar solo los valores proporcionados
    if "fullName" in data:
        user.full_name = data["fullName"]
    if "phoneNumber" in data:
        user.phone_number = data["phoneNumber"]
    if "dni" in data:
        user.dni = data["dni"]
    if "status" in data:
        user.status = data["status"]

    db.session.commit()

    return jsonify({"msg": "el usuario ha sido actualizado"}), 200


# Endpoint de Autenticación y generación de token
@users_bp.route('/users/auth', methods=['POST'])
def generate_token():
    data = request.get_json()

    # Validar que los campos requeridos estén presentes
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Debe proporcionar username y password"}), 400

    username = data["username"]
    password = data["password"]

    # Buscar usuario por username
    user = User.query.filter_by(username=username).first()

    # Validar credenciales
    if not user or not check_password_hash(user.password, password + user.salt):
        return jsonify({"error": "Credenciales incorrectas"}), 404

    # Generar token y fecha de expiración (1 hora de validez)
    token = secrets.token_hex(32)
    expire_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # Guardar el token en la base de datos
    user.token = token
    user.expire_at = expire_at
    db.session.commit()

    return jsonify({
        "id": str(user.id),
        "token": token,
        "expireAt": expire_at.isoformat()
    }), 200

# Middleware para autenticar el usuario mediante el token
def authenticate_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None, 403  # Código 403 si no hay token en el encabezado

    token = auth_header.split(" ")[1]  # Obtener el token después de "Bearer"
    user = User.query.filter_by(token=token).first()

    # Verificar si el token existe y no ha expirado
    if not user or not user.token or user.expire_at < datetime.datetime.utcnow():
        return None, 401  # Código 401 si el token no es válido o ha expirado

    return user, None

# Endpoint para obtener la información del usuario autenticado
@users_bp.route('/users/me', methods=['GET'])
def get_user_info():
    user, error_code = authenticate_user()
    if error_code:
        return jsonify({"error": "Token inválido o no autorizado"}), error_code

    return jsonify({
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "fullName": user.full_name,
        "dni": user.dni,
        "phoneNumber": user.phone_number,
        "status": user.status
    }), 200

# Endpoint para verificar que el servicio está activo
@users_bp.route('/users/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Users microservice is running"}), 200

# Endpoint para resetear la base de datos (solo pruebas)
@users_bp.route('/users/reset', methods=['POST'])
def reset_db():
    try:
        db.session.query(User).delete()
        db.session.commit()
        return jsonify({"message": "Database reset successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
