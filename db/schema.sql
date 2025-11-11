-- Companies
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    field TEXT
);

-- Users
-- company_id is NULL for superadmins (global users)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    status TEXT DEFAULT 'offline', -- online, offline (indicates if user is currently logged in)
    last_login TIMESTAMP, -- for statistics purposes
    company_id INT REFERENCES companies(id) ON DELETE CASCADE
);

-- Roles
-- Will contain values like: 'superadmin', 'company_admin', 'user'
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- User ↔ Role (many-to-many)
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE
);

-- Items (scoped per company)
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    sku TEXT NOT NULL,
    quantity INT DEFAULT 0,
    price NUMERIC(10,2),
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE
);

-- Orders (scoped per company, created by a user)
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status TEXT DEFAULT 'pending', -- pending, confirmed, shipped
    created_at TIMESTAMP DEFAULT now(),
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE
);

-- Order ↔ Item (many-to-many)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    quantity INT NOT NULL
);

-- Insert all roles
INSERT INTO roles (name) VALUES ('superadmin');
INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('manager');
INSERT INTO roles (name) VALUES ('employee');

-- Insert a superadmin user with password 'superadmin123'
INSERT INTO users (username, email, password_hash, company_id) VALUES (
    'superadmin',
    'superadmin@example.com',
    'scrypt:32768:8:1$VRMWaz97BQ7NYnNr$1c6a0e1e924fcdd3990d9df72610a538afad647a71d337e639e76b24a669f1bb3a8ace9185297c83a69606240ca7efb65f895294cdd3fa9f125b7fb4d88e62fa',
    NULL
);

-- Assign superadmin role to the superadmin user (assuming role id 1 is 'superadmin')
INSERT INTO user_roles (user_id, role_id) VALUES (1, 1);
