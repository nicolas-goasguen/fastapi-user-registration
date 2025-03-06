CREATE DOMAIN email AS TEXT CHECK (VALUE ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email email UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS verification_codes (
    id SERIAL PRIMARY KEY,
    email email REFERENCES users(email) ON DELETE CASCADE,
    code TEXT NOT NULL CHECK (LENGTH(code) = 4 AND code ~ '^[0-9]{4}$'),
    created_at TIMESTAMP DEFAULT NOW()
);
