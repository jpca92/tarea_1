# 📌 Creación de la tabla posts en PostgreSQL
CREATE TABLE IF NOT EXISTS posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id UUID NOT NULL,
    user_id UUID NOT NULL,
    expire_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

# 📌 Índices para mejorar la búsqueda
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_route_id ON posts(route_id);
CREATE INDEX IF NOT EXISTS idx_posts_expire_at ON posts(expire_at);