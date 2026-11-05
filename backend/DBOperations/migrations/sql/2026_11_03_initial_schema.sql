CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    login TEXT UNIQUE,
    hashed_password TEXT NOT NULL,
    name TEXT,
    email TEXT,
    is_verified BOOLEAN DEFAULT FALSE
);