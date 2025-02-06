-- Crear la función para actualizar automáticamente el campo updatedAt
CREATE OR REPLACE FUNCTION update_updatedAt_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Eliminar el trigger si ya existe
DROP TRIGGER IF EXISTS update_users_updatedAt ON users;

-- Crear el trigger
CREATE TRIGGER update_users_updatedAt
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updatedAt_column();