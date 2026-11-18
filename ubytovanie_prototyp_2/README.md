# SWI – Funkčný prototyp Flask + MySQL + Bootstrap

Prototyp pre **kapitolu 11.4** projektu *Žiadosť o ubytovanie B*. Demonštruje spoluprácu dvoch ArchiMate aplikačných komponentov. Bez WampServera, bez Node.js, bez frontendového build procesu.

## 1. Požiadavky

- Python 3.11+ (pri inštalácii vo Windows označte **Add Python to PATH**).
- MySQL Server 8.0+ (môže byť samostatne z MySQL Installer; alternatívne už bežiaci MySQL server).
- MySQL Workbench **alebo** príkazový klient `mysql` pre import SQL.
- Internet na prvú inštaláciu knižníc a zobrazenie Bootstrapu z CDN. Funkčná logika zostáva použiteľná aj bez načítaného CSS.

## 2. Vytvorenie databázy

1. Spustite službu **MySQL Server**. WampServer nie je potrebný.
2. Otvorte **MySQL Workbench** a prihláste sa administrátorským kontom k lokálnemu MySQL serveru.
3. `File → Open SQL Script...` → vyberte `databaza.sql` → kliknite na blesk **Execute**.
4. Súbor `prava.sql` obsahuje príklad vytvorenia samostatného databázového používateľa `swi_demo`. **Najprv v ňom nahraďte `ZMENTE_HESLO` vlastným silným heslom**, potom skript spustite ako administrátor. Ak už takého používateľa máte, namiesto vytvorenia nového používateľa upravte jeho prístupové údaje podľa svojho MySQL nastavenia.
5. Overte, že v databáze `swi_prototyp` existujú tabuľky `pouzivatel`, `akademicky_rok` a `ziadost`.

Prípadne príkazový riadok (ak máte `mysql` dostupný v PATH):

```powershell
mysql -u root -p < databaza.sql
mysql -u root -p < prava.sql
```

Príkazy s `<` používajte vo Windows **CMD**, nie v PowerShelli. V MySQL Workbench importujte skripty cez editor.

## 3. Inštalácia aplikácie – Windows PowerShell

Rozbaľte ZIP napríklad do `C:\SWI_Flask_MySQL_Bootstrap` a otvorte terminál v priečinku projektu:

```powershell
cd C:\SWI_Flask_MySQL_Bootstrap
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

V `.env` nastavte `MYSQL_USER`, `MYSQL_PASSWORD` a prípadne port podľa svojho servera. Hodnota `FLASK_SECRET_KEY` má byť ľubovoľný dlhý náhodný reťazec. Tento súbor **neodovzdávajte a nenahrávajte na GitHub**.

Spustenie:

```powershell
.\.venv\Scripts\python.exe app.py
```

Otvorte **http://127.0.0.1:5000/**. Flask bude lokálne bežať len počas otvoreného terminálu. Vypnutie: `Ctrl+C`.

Ak nemáte príkaz `py`, použite `python`.

### macOS/Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# upravte .env
.venv/bin/python app.py
```

MySQL server musí bežať aj na týchto systémoch.

## 4. Demonštračné scenáre

Súbor `databaza.sql` pripraví **dva testovacie akademické roky** s termínmi počítanými od času importu. Žiadosti evidujeme pre simulovanú identitu `DEMO-STUDENT-001`.

1. **Úspešná evidencia** – vyberte `TEST-OTVORENE`, potvrďte. Výsledok: nová žiadosť v stave `Rozpracovana` a jej ID.
2. **Neúspech: uzávierka** – vyberte `TEST-PO-UZAVIERKE`, potvrďte. Výsledok: odmietnutie a žiadna nová žiadosť.
3. **Neúspech: duplicita** – znova vyberte `TEST-OTVORENE`. Výsledok: oznámenie o pôvodnej žiadosti, bez nového záznamu.

**Po druhom a treťom scenári** overte v MySQL Workbench, že počet žiadostí sa nezmenil:

```sql
USE swi_prototyp;
SELECT id_ziadost, id_pouzivatel, id_akademicky_rok, stav, cas_vytvorenia FROM ziadost ORDER BY id_ziadost;
```

Na opakovanie scenárov spustite `reset_demo.sql` v MySQL Workbench. Pozor: odstráni demonštračné žiadosti testovacieho študenta.

## 5. Súlad s ArchiMate

| ArchiMate prvok | Implementácia |
| --- | --- |
| Konfigurácia akademického roka (komponent) | `KonfiguraciaRoka.py` / trieda `KonfiguraciaRoka` |
| Správa žiadostí a podkladov (komponent) | `SpravaZiadosti.py` / trieda `SpravaZiadosti` |
| Poskytnúť pravidlá podávania (služba) | `KonfiguraciaRoka.ziskajPravidlaPodavania()` |
| Evidovať podanie žiadosti (služba) | `SpravaZiadosti.podajZiadost()` |
| Pravidlá podania (dátový objekt) | dáta `akademicky_rok`, výsledok `dict` v Pythone |
| Žiadosti o ubytovanie (dátový objekt) | dáta `ziadost`, záznamy načítané do `dict` |
| Serving – poskytovanie služby | volanie `self.konfiguracia_roka.ziskajPravidlaPodavania(...)` v `SpravaZiadosti.py` |

**Hranica prototypu:** Úspešný scenár vytvára rozpracovanú žiadosť, NIE kompletné oficiálne podanie. AIS, 2FA, prílohy ani konečné prideľovanie sa neimplementujú; externá identita je simulovaná testovacím používateľom.

## 6. Jednotkové testy

Po inštalácii knižníc:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tieto testy simulujú databázové spojenie. **Nenahrádzajú** funkčnú demonštráciu nad bežiacou MySQL.

## 7. Časté problémy

- `ModuleNotFoundError`: nainštalujte závislosti pomocou `.venv` Pythonu ako v kroku 3.
- `Access denied for user`: skontrolujte `MYSQL_USER`, `MYSQL_PASSWORD`, granty a príslušný host `localhost`/`127.0.0.1`.
- `Can't connect to MySQL server`: skontrolujte bežiaci MySQL Server a port `3306`.
- `Unknown database` alebo chýbajúce tabuľky: spustite `databaza.sql`.
- Chyba portu `5000`: zmeňte parameter `port=5000` v poslednom riadku `app.py`.
- Stránka nemá Bootstrap dizajn: na prvé načítanie Bootstrap CSS z CDN je potrebné internetové pripojenie.


## Poznámka k bezpečnosti

Toto je iba lokálny prototyp. Nepoužívajte ho s reálnymi osobnými údajmi, neukladajte heslá do kódu a nespúšťajte Flask vývojový server verejne!!!
