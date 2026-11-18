-- Import cez MySQL Workbench alebo prikazovy riadok. Bez WampServera.
-- Testovacie terminy su relativne k okamihu importu.
CREATE DATABASE IF NOT EXISTS swi_prototyp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE swi_prototyp;

CREATE TABLE IF NOT EXISTS pouzivatel (
 id_pouzivatel INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 univerzitny_identifikator VARCHAR(80) NOT NULL UNIQUE,
 meno VARCHAR(100) NOT NULL,
 priezvisko VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS akademicky_rok (
 id_akademicky_rok INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 nazov VARCHAR(50) NOT NULL UNIQUE,
 zaciatok_podavania DATETIME NOT NULL,
 uzavierka_podavania DATETIME NOT NULL,
 CONSTRAINT chk_terminy CHECK (uzavierka_podavania > zaciatok_podavania)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ziadost (
 id_ziadost INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 id_pouzivatel INT NOT NULL,
 id_akademicky_rok INT NOT NULL,
 stav VARCHAR(40) NOT NULL DEFAULT 'Rozpracovana',
 cas_vytvorenia DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT fk_ziadost_pouzivatel FOREIGN KEY (id_pouzivatel) REFERENCES pouzivatel(id_pouzivatel),
 CONSTRAINT fk_ziadost_rok FOREIGN KEY (id_akademicky_rok) REFERENCES akademicky_rok(id_akademicky_rok),
 CONSTRAINT uq_jeden_student_rok UNIQUE (id_pouzivatel, id_akademicky_rok)
) ENGINE=InnoDB;

INSERT INTO pouzivatel (univerzitny_identifikator, meno, priezvisko)
VALUES ('DEMO-STUDENT-001', 'Testovací', 'Študent')
ON DUPLICATE KEY UPDATE meno = 'Testovací', priezvisko = 'Študent';

INSERT INTO akademicky_rok (nazov, zaciatok_podavania, uzavierka_podavania)
VALUES
 ('TEST-OTVORENE', DATE_SUB(NOW(), INTERVAL 7 DAY), DATE_ADD(NOW(), INTERVAL 7 DAY)),
 ('TEST-PO-UZAVIERKE', DATE_SUB(NOW(), INTERVAL 14 DAY), DATE_SUB(NOW(), INTERVAL 7 DAY))
ON DUPLICATE KEY UPDATE
 zaciatok_podavania = VALUES(zaciatok_podavania),
 uzavierka_podavania = VALUES(uzavierka_podavania);
