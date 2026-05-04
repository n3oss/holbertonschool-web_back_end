-- Creates a table 'users' with a unique email requirement.
-- The script will not fail if the table already exists
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
