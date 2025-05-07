CREATE EXTENSION IF NOT EXISTS citext;

CREATE DOMAIN email_address AS citext CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$');
CREATE DOMAIN code_4_digits AS TEXT CHECK (LENGTH(VALUE) = 4 AND VALUE ~ '^[0-9]{4}$');

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email email_address UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE
);
-- speeds up searches for inactive users
CREATE INDEX idx_users_is_active ON users(is_active);

CREATE TABLE IF NOT EXISTS verification_codes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    code code_4_digits NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
 -- speeds up searches for user_id, user_id + code, user_id + code + created_at
CREATE INDEX idx_verification_codes_created_at ON verification_codes(created_at);
CREATE INDEX idx_verification_codes_user_id_code_created_at ON verification_codes(user_id, code, created_at);
ALTER TABLE verification_codes
    ADD CONSTRAINT chk_created_at_not_in_future CHECK (created_at <= NOW());

CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule(
    '*/5 * * * *',
    $$
    DELETE FROM verification_codes
    WHERE created_at < NOW() - INTERVAL '2 minutes';
    $$
);
