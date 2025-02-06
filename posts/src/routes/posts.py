from flask import Blueprint, request, jsonify
from models import Post
from db import db
from datetime import datetime
from auth import authenticate_user  # el middleware de autenticación id
import uuid

posts_bp = Blueprint('posts', __name__)

# Validación de UUID
def is_valid_uuid(value):
    try:
        return str(uuid.UUID(str(value))) == value
    except (ValueError, TypeError):
        return False

# Endpoint para crear una publicación
@posts_bp.route('/posts', methods=['POST'])
def create_post():
    user, error_code = authenticate_user()
    if error_code or not user:
        return jsonify({"error": "Token inválido o no autorizado"}), error_code or 403

    data = request.json
    required_fields = ["routeId", "expireAt"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "routeId y expireAt son obligatorios"}), 400

    # Validar que routeId sea un UUID válido
    if not is_valid_uuid(data["routeId"]):
        return jsonify({"error": "routeId debe ser un UUID válido"}), 400

    # Validar formato y valor de expireAt
    try:
        expire_at = datetime.fromisoformat(data["expireAt"])
        if expire_at <= datetime.utcnow():
            return jsonify({"msg": "La fecha de expiración no es válida"}), 412
    except ValueError:
        return jsonify({"msg": "Formato de fecha inválido"}), 412

    # Crear la nueva publicación
    new_post = Post(
        route_id=uuid.UUID(data["routeId"]),
        user_id=uuid.UUID(user.get("id")),
        expire_at=expire_at
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "id": str(new_post.id),
        "userId": str(new_post.user_id),
        "createdAt": new_post.created_at.isoformat() + "Z"
    }), 201

# Endpoint para ver y filtrar publicaciones
@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    user, error_code = authenticate_user()
    if error_code or not user:
        return jsonify({"error": "Token inválido o no autorizado"}), error_code or 403

    expire_filter = request.args.get("expire")
    route_filter = request.args.get("route")
    owner_filter = request.args.get("owner")

    query = Post.query

    if expire_filter is not None:
        expire_bool = expire_filter.lower() == "true"
        query = query.filter((Post.expire_at < datetime.utcnow()) if expire_bool else (Post.expire_at >= datetime.utcnow()))

    if route_filter:
        if is_valid_uuid(route_filter):
            query = query.filter(Post.route_id == uuid.UUID(route_filter))
        else:
            return jsonify({"error": "route debe ser un UUID válido"}), 400

    if owner_filter:
        if owner_filter.lower() == "me":
            query = query.filter(Post.user_id == uuid.UUID(user.get("id")))
        elif is_valid_uuid(owner_filter):
            query = query.filter(Post.user_id == uuid.UUID(owner_filter))
        else:
            return jsonify({"error": "owner debe ser 'me' o un UUID válido"}), 400

    posts = query.all()

    return jsonify([
        {
            "id": str(post.id),
            "routeId": str(post.route_id),
            "userId": str(post.user_id),
            "expireAt": post.expire_at.isoformat() + "Z",
            "createdAt": post.created_at.isoformat() + "Z"
        } for post in posts
    ]), 200

# Endpoint para consultar una publicación específica
@posts_bp.route('/posts/<uuid:id>', methods=['GET'])
def get_post(id):
    user, error_code = authenticate_user()
    if error_code or not user:
        return jsonify({"error": "Token inválido o no autorizado"}), error_code or 403

    post = Post.query.get(id)

    if not post:
        return jsonify({"error": "Publicación no encontrada"}), 404

    return jsonify({
        "id": str(post.id),
        "routeId": str(post.route_id),
        "userId": str(post.user_id),
        "expireAt": post.expire_at.isoformat() + "Z",
        "createdAt": post.created_at.isoformat() + "Z"
    }), 200

# Endpoint para eliminar una publicación
@posts_bp.route('/posts/<uuid:id>', methods=['DELETE'])
def delete_post(id):
    user, error_code = authenticate_user()
    if error_code or not user:
        return jsonify({"error": "Token inválido o no autorizado"}), error_code or 403

    post = Post.query.get(id)

    if not post:
        return jsonify({"error": "Publicación no encontrada"}), 404

    # Validación de permisos
    if str(post.user_id) != str(user.get("id")):
        return jsonify({"error": "No tienes permiso para eliminar esta publicación"}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({"msg": "La publicación fue eliminada"}), 200

# Endpoint para verificar la salud del servicio
@posts_bp.route('/posts/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Posts microservice is running"}), 200

# Endpoint para resetear la base de datos (solo pruebas)
@posts_bp.route('/posts/reset', methods=['POST'])
def reset_db():
    try:
        db.session.query(Post).delete()
        db.session.commit()
        return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
