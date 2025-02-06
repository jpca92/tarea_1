-- Crear la tabla routes
CREATE TABLE IF NOT EXISTS routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_id VARCHAR(50) UNIQUE NOT NULL,
    source_airport_code VARCHAR(10) NOT NULL,
    source_country VARCHAR(100) NOT NULL,
    destiny_airport_code VARCHAR(10) NOT NULL,
    destiny_country VARCHAR(100) NOT NULL,
    bag_cost INTEGER NOT NULL CHECK (bag_cost >= 0),
    planned_start_date TIMESTAMP NOT NULL CHECK (planned_start_date > NOW()),
    planned_end_date TIMESTAMP NOT NULL CHECK (planned_end_date > planned_start_date),
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Índice para búsqueda rápida por flight_id
CREATE INDEX IF NOT EXISTS idx_routes_flight_id ON routes (flight_id);
