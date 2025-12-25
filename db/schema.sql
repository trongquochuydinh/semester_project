-- =========================
-- DATABASE SCHEMA
-- Single role per user
-- =========================

-- -------------------------
-- Companies
-- -------------------------
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    field TEXT
);

INSERT INTO companies (name, field)
VALUES ('TechNova', 'Software Development');

-- -------------------------
-- Roles (MUST come before users)
-- -------------------------
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

INSERT INTO roles (name) VALUES
('superadmin'),
('admin'),
('manager'),
('employee');

-- -------------------------
-- Users
-- -------------------------
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,

    status TEXT DEFAULT 'offline',
    last_login TIMESTAMP,

    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
    role_id INT NOT NULL REFERENCES roles(id)
);

-- -------------------------
-- Seed users
-- -------------------------

-- superadmin (global)
INSERT INTO users (username, email, password_hash, company_id, role_id)
VALUES (
    'superadmin',
    'superadmin@example.com',
    'scrypt:32768:8:1$VRMWaz97BQ7NYnNr$1c6a0e1e924fcdd3990d9df72610a538afad647a71d337e639e76b24a669f1bb3a8ace9185297c83a69606240ca7efb65f895294cdd3fa9f125b7fb4d88e62fa',
    NULL,
    1
);

-- admin
INSERT INTO users (username, email, password_hash, company_id, role_id)
VALUES (
    'admin',
    'admin@technova.com',
    'scrypt:32768:8:1$LAYR5AP8fD3IzoXE$e01c29446bc30a71d6436957af1f040349bfeee2d5bd3ead05fff29184c0bf82ee0846af695af2e9941bce4b20eb84f5a2dbb88271c167e6f2ba4180a1a1f75f',
    1,
    2
);

-- manager
INSERT INTO users (username, email, password_hash, company_id, role_id)
VALUES (
    'manager',
    'manager@technova.com',
    'scrypt:32768:8:1$YhN1PkULDrlbixbX$3c01b8e19795cd749392d3d6cf6b96e96495ca4e114cbe306ebc4369ccdbf88c618564698c324cd2146e927cdd32cc4e2d52f2941ef10edececc9d6381550d9a',
    1,
    3
);

-- employee
INSERT INTO users (username, email, password_hash, company_id, role_id)
VALUES (
    'employee',
    'employee@technova.com',
    'scrypt:32768:8:1$DsZHzDPxZbEYOg1b$a9aa837ce7b598eba46310616d8fc87ec0f91a40d28607e31fd48492e891fba4ad4a863288c6b90169f7de75159f683c90187c20a28a65bb48e1d441d9e411d5',
    1,
    4
);

-- -------------------------
-- Items
-- -------------------------
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    sku TEXT NOT NULL,
    quantity INT DEFAULT 0,
    price NUMERIC(10,2),
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE
);

-- -------------------------
-- Orders
-- -------------------------
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT now(),

    user_id INT NOT NULL REFERENCES users(id),
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE
);

-- -------------------------
-- Order items
-- -------------------------
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    quantity INT NOT NULL
);
