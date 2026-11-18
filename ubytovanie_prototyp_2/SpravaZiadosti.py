"""ArchiMate aplikačný komponent: Správa žiadostí a podkladov."""
from mysql.connector import IntegrityError


class SpravaZiadosti:
    def __init__(self, otvor_spojenie, konfiguracia_roka):
        self.otvor_spojenie = otvor_spojenie
        self.konfiguracia_roka = konfiguracia_roka

    def podajZiadost(self, id_pouzivatel, id_akademicky_rok):
        """Aplikačná služba: Evidovať podanie žiadosti (iba simulácia).

        V skutočnosti vzniká Rozpracovana, nie oficiálne Podana.
        Návrat: dict {typ, sprava, id_ziadost}.
        """
        # Priame prepojenie dvoch komponentov podľa ArchiMate modelu:
        pravidla = self.konfiguracia_roka.ziskajPravidlaPodavania(
            id_akademicky_rok)
        if pravidla is None:
            return {"typ": "chyba",
                    "sprava": "Akademický rok sa nenašiel.",
                    "id_ziadost": None}

        teraz = pravidla["aktualny_cas"]
        if not (pravidla["zaciatok_podavania"] <= teraz < pravidla["uzavierka_podavania"]):
            return {"typ": "chyba", "sprava": "Podávanie nie je otvorené alebo už uplynula uzávierka.", "id_ziadost": None}

        conn = self.otvor_spojenie()
        try:
            cur = conn.cursor(dictionary=True)
            try:
                # Opakovaný pokus nesmie vytvoriť duplicitu.
                cur.execute(
                    "SELECT id_ziadost FROM ziadost WHERE id_pouzivatel=%s AND id_akademicky_rok=%s",
                    (id_pouzivatel, id_akademicky_rok),
                )
                povodna = cur.fetchone()
                if povodna:
                    return {"typ": "upozornenie", "sprava": "Žiadosť pre tento akademický rok už existuje. Nový záznam nevznikol.", "id_ziadost": povodna["id_ziadost"]}

                try:
                    cur.execute(
                        """INSERT INTO ziadost (id_pouzivatel, id_akademicky_rok, stav)
                           VALUES (%s, %s, 'Rozpracovana')""",
                        (id_pouzivatel, id_akademicky_rok),
                    )
                    nove_id = cur.lastrowid
                    conn.commit()
                except IntegrityError as exc:
                    conn.rollback()
                    # Databázový UNIQUE chráni aj proti súbežnému podaniu.
                    if exc.errno != 1062:
                        raise
                    cur.execute(
                        "SELECT id_ziadost FROM ziadost WHERE id_pouzivatel=%s AND id_akademicky_rok=%s",
                        (id_pouzivatel, id_akademicky_rok),
                    )
                    povodna = cur.fetchone()
                    return {"typ": "upozornenie", "sprava": "Žiadosť už existuje. Nový záznam nevznikol.", "id_ziadost": povodna["id_ziadost"] if povodna else None}

                return {"typ": "uspech", "sprava": "Rozpracovaná žiadosť bola úspešne vytvorená.", "id_ziadost": nove_id}
            finally:
                cur.close()
        finally:
            conn.close()

    def ziskajZiadosti(self, id_pouzivatel):
        conn = self.otvor_spojenie()
        try:
            cur = conn.cursor(dictionary=True)
            try:
                cur.execute(
                    """SELECT z.id_ziadost, a.nazov AS akademicky_rok, z.stav, z.cas_vytvorenia
                       FROM ziadost z JOIN akademicky_rok a ON a.id_akademicky_rok=z.id_akademicky_rok
                       WHERE z.id_pouzivatel=%s ORDER BY z.id_ziadost DESC""",
                    (id_pouzivatel,),
                )
                return cur.fetchall()
            finally:
                cur.close()
        finally:
            conn.close()
