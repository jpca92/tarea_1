from dotenv import load_dotenv
import os

class Config:
    """Configuración de la aplicación y base de datos."""

    # Cargar variables desde el archivo .env y forzar su carga
    load_dotenv(override=True)

    # Depuración: Imprimir valores de entorno cargados
    print("[*] DB_USER:", os.getenv("DB_USER"))
    print("[*] DB_PASSWORD:", os.getenv("DB_PASSWORD"))
    print("[*] DB_NAME:", os.getenv("DB_NAME"))
    print("[*] DB_HOST:", os.getenv("DB_HOST"))
    print("[*] DB_PORT:", os.getenv("DB_PORT"))

    # Construir la URI de conexión
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Imprimir la URI construida
    print(f"[*] Conectando a la base de datos: {SQLALCHEMY_DATABASE_URI}")


