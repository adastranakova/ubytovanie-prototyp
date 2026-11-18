"""Lokálna webová demonštrácia architektonického prototypu SWI."""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import Error as MySQLError
from dotenv import load_dotenv
from databaza import spojenie
from KonfiguraciaRoka import KonfiguraciaRoka
from SpravaZiadosti import SpravaZiadosti

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "LEN_PRE_LOKALNU_DEMONSTRACIU")

konfiguracia = KonfiguraciaRoka(spojenie)
sprava = SpravaZiadosti(spojenie, konfiguracia)
TESTOVACI_STUDENT = "DEMO-STUDENT-001"  # Simulácia externej univerzitnej identity


def nacitaj_podklady():
    conn = spojenie()
    try:
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_pouzivatel, meno, priezvisko FROM pouzivatel WHERE univerzitny_identifikator=%s", (TESTOVACI_STUDENT,))
            student = cur.fetchone()
            cur.execute("SELECT id_akademicky_rok, nazov, zaciatok_podavania, uzavierka_podavania, NOW() AS aktualny_cas FROM akademicky_rok ORDER BY id_akademicky_rok")
            roky = cur.fetchall()
            return student, roky
        finally:
            cur.close()
    finally:
        conn.close()


@app.get("/")
def index():
    try:
        student, roky = nacitaj_podklady()
        ziadosti = sprava.ziskajZiadosti(student["id_pouzivatel"]) if student else []
        return render_template("index.html", student=student, roky=roky, ziadosti=ziadosti, db_chyba=None)
    except MySQLError:
        return render_template("index.html", student=None, roky=[], ziadosti=[], db_chyba="Nedá sa pripojiť k databáze. Skontrolujte MySQL a súbor .env."), 503


@app.post("/evidovat")
def evidovat():
    try:
        id_roka = int(request.form.get("id_akademicky_rok", ""))
    except (ValueError, TypeError):
        flash("Vyberte platný akademický rok.", "danger")
        return redirect(url_for("index"))
    try:
        student, _ = nacitaj_podklady()
        if student is None:
            flash("Testovací študent sa nenašiel. Importujte databaza.sql.", "danger")
        else:
            vysledok = sprava.podajZiadost(student["id_pouzivatel"], id_roka)
            kategoria = {"uspech": "success", "upozornenie": "warning", "chyba": "danger"}[vysledok["typ"]]
            suffix = f" ID žiadosti: {vysledok['id_ziadost']}." if vysledok["id_ziadost"] is not None else ""
            flash(vysledok["sprava"] + suffix, kategoria)
    except MySQLError:
        flash("Databázová chyba. Skontrolujte pripojenie alebo štruktúru tabuliek.", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
