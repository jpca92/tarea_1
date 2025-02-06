import requests
import os
from flask import request

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://users:5000")

def authenticate_user():
    """Verifica el token con el microservicio de users y obtiene el user_id."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None, 403  # No hay token en la solicitud

    token = auth_header.split(" ")[1]

    # Consultar users para validar el token y obtener el user_id
    try:
        response = requests.get(f"{USERS_SERVICE_URL}/users/me", headers={"Authorization": f"Bearer {token}"})
        
        if response.status_code == 200:
            user_data = response.json()
            return user_data, None  # Retorna user_id y otros datos
        elif response.status_code in [401, 403]:
            return None, response.status_code
        else:
            return None, 500  # Error interno
    except requests.exceptions.RequestException:
        return None, 500  # Error en la conexión con `users`

