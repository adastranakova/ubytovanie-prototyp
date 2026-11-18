"""Jednotkové testy troch scenárov bez skutočnej MySQL databázy.
Spustenie: python -m unittest discover -s tests -v
Integračné overenie nad MySQL je potrebné vykonať samostatne.
"""
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from SpravaZiadosti import SpravaZiadosti


class Scenare(unittest.TestCase):
    def setUp(self):
        self.t = datetime(2026, 11, 18, 12, 0)
        self.konfiguracia = MagicMock()
        self.konfiguracia.ziskajPravidlaPodavania.return_value = {
            "zaciatok_podavania": self.t - timedelta(days=3),
            "uzavierka_podavania": self.t + timedelta(days=3),
            "aktualny_cas": self.t,
        }
        self.conn = MagicMock()
        self.cur = MagicMock()
        self.conn.cursor.return_value = self.cur
        self.sprava = SpravaZiadosti(lambda: self.conn, self.konfiguracia)

    def test_uspesna_evidencia(self):
        self.cur.fetchone.return_value = None
        self.cur.lastrowid = 12
        vysledok = self.sprava.podajZiadost(1, 2)
        self.assertEqual(vysledok["typ"], "uspech")
        self.assertEqual(vysledok["id_ziadost"], 12)
        self.conn.commit.assert_called_once()
        self.konfiguracia.ziskajPravidlaPodavania.assert_called_once_with(2)

    def test_po_uzavierke(self):
        self.konfiguracia.ziskajPravidlaPodavania.return_value["uzavierka_podavania"] = self.t
        vysledok = self.sprava.podajZiadost(1, 2)
        self.assertEqual(vysledok["typ"], "chyba")
        self.conn.cursor.assert_not_called()

    def test_duplicita(self):
        self.cur.fetchone.return_value = {"id_ziadost": 10}
        vysledok = self.sprava.podajZiadost(1, 2)
        self.assertEqual(vysledok["typ"], "upozornenie")
        self.assertEqual(vysledok["id_ziadost"], 10)
        self.conn.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
