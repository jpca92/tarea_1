-- Crear la tabla users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(15),  -- Cambiado de phonenumber a phone_number
    dni VARCHAR(20),
    full_name VARCHAR(100),  -- Cambiado de fullname a full_name
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    token VARCHAR(255),
    status VARCHAR(20) NOT NULL CHECK (status IN ('POR_VERIFICAR', 'NO_VERIFICADO', 'VERIFICADO')),
    expire_at TIMESTAMP,  -- Cambiado de expireAt a expire_at
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- Cambiado de createdAt a created_at
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Cambiado de updatedAt a updated_at
);


-- Crear índices
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);