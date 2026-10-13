CREATE DATABASE IF NOT EXISTS ubytovanie_prototyp
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ubytovanie_prototyp;

CREATE TABLE IF NOT EXISTS internat (
    id INT PRIMARY KEY,
    nazov VARCHAR(100) NOT NULL
);

INSERT INTO internat (id, nazov)
SELECT 1, 'Internát A'
WHERE NOT EXISTS (
    SELECT 1 FROM internat WHERE id = 1
);
