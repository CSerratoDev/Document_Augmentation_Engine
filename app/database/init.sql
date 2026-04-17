CREATE EXTENSION IF NOT EXISTS citext;

DROP TABLE IF EXISTS company_documents CASCADE;
DROP TABLE IF EXISTS company_agents CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

DROP TYPE IF EXISTS user_role;

CREATE TYPE user_role AS ENUM ('client', 'seller');

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email CITEXT NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role user_role NOT NULL DEFAULT 'client'
);

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE company_agents (
    company_id INT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    PRIMARY KEY(company_id, user_id)
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_extension VARCHAR(5) NOT NULL, -- pdf, txt
    file_data BYTEA,
    file_url TEXT,
    company_id INT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "user" (name, email, password, role)
VALUES
    ('Admin User', 'admin@example.com', 'admin123', 'seller'),
    ('Juan Pérez', 'juan.perez@example.com', 'pass1', 'seller');

INSERT INTO company (name)
VALUES
    ('ABC'),
    ('Software');

INSERT INTO company_agents (company_id, user_id)
VALUES
    (1, 1),
    (2, 2);

INSERT INTO documents (file_name, file_extension, company_id, file_url)
VALUES
    ('contrato_empleado', 'pdf', 1, 'https://storage.com/c21/doc1.pdf'),
    ('inventario_software', 'txt', 2, 'https://storage.com/hu/doc2.txt');