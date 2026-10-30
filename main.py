import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)
PLIK_BAZY = 'baza.json'

def wczytaj_historie():
    if not os.path.exists(PLIK_BAZY):
        return {}
    try:
        with open(PLIK_BAZY, 'r', encoding='utf-8') as plik:
            return json.load(plik)
    except (json.JSONDecodeError, IOError):
        return {}

def zapisz_historie():
    with open(PLIK_BAZY, 'w', encoding='utf-8') as plik:
        json.dump(dane, plik, indent=4, ensure_ascii=False)
@app.route('/')
def index():
    dane_z_pythona = "Witaj na stronie!"
    return render_template('index.html', tekst=dane_z_pythona)

@app.route('/', methods=['GET', 'POST'])

def kalkulator_godzin_kodland():
    historia = wczytaj_historie()
    if request.method == 'POST':
        nazwy_lekcji = {
            'lekcja_indywidualna': 28.50,
            'lekcja_1_1': 39.00,
            'zajecia_grupowe': 52.00,
            'zajecia_grupowe_zaawansowane': 68.00
        }
        sumowanie = 0
        for nazwa, cena in nazwy_lekcji:
            wartosc_z_html = request.form.get(nazwa)
            if wartosc_z_html:
                ilosc_lekcji = int(wartosc_z_html)
                koszt_lekcji = ilosc_lekcji * cena
                sumowanie += koszt_lekcji

        ilosc_lekcji_indywidualnych = request.form.get('lekcja_indywidualna')
        ilosc_lekcji_1_1 = request.form.get('lekcja_1_1')
        ilosc_zajec_grupowych = request.form.get('zajecia_grupowe')
        ilosc_zajec_grupowych_zaawansowanych = request.form.get('zajecia_grupowe_zaawansowane')

        odpowiedz = f"Suma = {sumowanie}"
        return odpowiedz


if __name__ == '__main__':
    app.run(debug=True)