"""ArchiMate aplikačný komponent: Konfigurácia akademického roka."""


class KonfiguraciaRoka:
    def __init__(self, otvor_spojenie):
        self.otvor_spojenie = otvor_spojenie

    def ziskajPravidlaPodavania(self, id_akademicky_rok):
        """Aplikačná služba: Poskytnúť pravidlá podávania.

        Vracia dátový objekt Pravidlá podania vrátane času databázového servera.
        """
        conn = self.otvor_spojenie()
        try:
            cur = conn.cursor(dictionary=True)
            try:
                cur.execute(
                    """SELECT id_akademicky_rok, nazov, zaciatok_podavania,
                              uzavierka_podavania, NOW() AS aktualny_cas
                       FROM akademicky_rok WHERE id_akademicky_rok = %s""",
                    (id_akademicky_rok,),
                )
                return cur.fetchone()
            finally:
                cur.close()
        finally:
            conn.close()
