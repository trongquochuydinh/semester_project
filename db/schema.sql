-- Companies
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    industry TEXT
);

-- Users
-- company_id is NULL for superadmins (global users)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
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

-- Insert a superadmin user (replace <hash> with a real hash from werkzeug.security.generate_password_hash)
INSERT INTO users (username, email, password_hash, company_id) VALUES ('superadmin', 'superadmin@example.com', '$pbkdf2-sha256$29000$examplehash', NULL);

-- Assign superadmin role to the superadmin user (assuming role id 1 is 'superadmin')
INSERT INTO user_roles (user_id, role_id) VALUES (1, 1);
