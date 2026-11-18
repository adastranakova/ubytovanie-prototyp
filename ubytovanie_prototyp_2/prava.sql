-- SPUSTITE ako MySQL administrator. Heslo ZMENTE_HESLO nahradte svojím vlastným.
CREATE USER IF NOT EXISTS 'swi_demo'@'localhost' IDENTIFIED BY 'ZMENTE_HESLO';
GRANT SELECT, INSERT, UPDATE, DELETE ON swi_prototyp.* TO 'swi_demo'@'localhost';
-- Ak pouzivate MYSQL_HOST=127.0.0.1 a MySQL server rozlisuje localhost od 127.0.0.1:
CREATE USER IF NOT EXISTS 'swi_demo'@'127.0.0.1' IDENTIFIED BY 'ZMENTE_HESLO';
GRANT SELECT, INSERT, UPDATE, DELETE ON swi_prototyp.* TO 'swi_demo'@'127.0.0.1';
