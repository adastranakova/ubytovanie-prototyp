-- Pozor: vymaze LEN demonštracne ziadosti testovacieho studenta!
USE swi_prototyp;
DELETE z FROM ziadost z JOIN pouzivatel p ON p.id_pouzivatel=z.id_pouzivatel
WHERE p.univerzitny_identifikator='DEMO-STUDENT-001';
UPDATE akademicky_rok SET zaciatok_podavania=DATE_SUB(NOW(), INTERVAL 7 DAY), uzavierka_podavania=DATE_ADD(NOW(), INTERVAL 7 DAY) WHERE nazov='TEST-OTVORENE';
UPDATE akademicky_rok SET zaciatok_podavania=DATE_SUB(NOW(), INTERVAL 14 DAY), uzavierka_podavania=DATE_SUB(NOW(), INTERVAL 7 DAY) WHERE nazov='TEST-PO-UZAVIERKE';
