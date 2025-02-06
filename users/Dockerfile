# Usa una imagen base ligera de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias primero (para aprovechar la caché)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de `src/` a `/app/` en lugar de copiar la carpeta completa
COPY src/ /app/

ENV FLASK_ENV=testing
ENV PYTHONPATH=/app

# Exponer el puerto que usa la aplicación
EXPOSE $CONFIG_PORT

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]


