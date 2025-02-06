FROM postgres:latest

# Configurar variables de entorno dinámicamente (sin hardcodear contraseñas)
ENV POSTGRES_DB=${DB_NAME}
ENV POSTGRES_USER=${DB_USER}
ENV POSTGRES_PASSWORD=${DB_PASSWORD}

# Copiar los scripts SQL de inicialización
COPY 01_create_table_users.sql /docker-entrypoint-initdb.d/
COPY 02_create_triggers_users.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de PostgreSQL
EXPOSE ${DB_PORT}