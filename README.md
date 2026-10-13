# Žiadosť o ubytovanie B – triviálny prototyp

## Cieľ
Overiť prepojenie PHP stránky s databázou MySQL.
Stránka zobrazí názov internátu načítaný z databázy.

## Potrebné prostredie
- WampServer s PHP a MySQL
- Webový prehliadač

## Spustenie
1. Umiestnite projekt do priečinka www WampServera.
2. Spustite WampServer.
3. V phpMyAdmin na serveri MySQL vykonajte database.sql.
4. Skopírujte config.example.php ako config.php.
5. V config.php nastavte používateľa, heslo a port MySQL.
6. Otvorte http://localhost/ubytovanie-prototyp/.

Ak Apache používa iný port, upravte adresu.

## Overenie
V databáze zmeňte názov internátu s ID 1.
Po obnovení stránky sa **MUSÍ** zobraziť nový názov.

## Rozsah
Prototyp obsahuje jednu tabuľku a jednu stránku.
