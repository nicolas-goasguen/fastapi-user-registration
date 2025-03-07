CREATE EXTENSION IF NOT EXISTS citext;

CREATE DOMAIN email_address AS citext CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$');
CREATE DOMAIN code_4_digits AS TEXT CHECK (LENGTH(VALUE) = 4 AND VALUE ~ '^[0-9]{4}$');

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email email_address UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS verification_codes (
    id SERIAL PRIMARY KEY,
    user_id SERIAL REFERENCES users(id) ON DELETE CASCADE,
    code code_4_digits NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
