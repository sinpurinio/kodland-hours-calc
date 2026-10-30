import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
PLIK_BAZY = 'baza.json'


def wczytaj_historie():
    if not os.path.exists(PLIK_BAZY):
        return []
    try:
        with open(PLIK_BAZY, 'r', encoding='utf-8') as plik:
            return json.load(plik)
    except (json.JSONDecodeError, IOError):
        return []

def zapisz_historie(dane):
    with open(PLIK_BAZY, 'w', encoding='utf-8') as plik:
        json.dump(dane, plik, indent=4, ensure_ascii=False)

@app.route('/wyczysc', methods=['POST'])
def wyczysc_historie():
    zapisz_historie([])  # Nadpisujemy baza.json pustą listą []
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def kalkulator_godzin_kodland():
    historia = wczytaj_historie()
    wynik = None

    if request.method == 'POST':
        nazwy_lekcji = {
            'lekcja_indywidualna': 28.50,
            'lekcja_1_1': 39.00,
            'zajecia_grupowe': 52.00,
            'zajecia_grupowe_zaawansowane': 68.00
        }
        sumowanie = 0
        szczegoly = {}

        for nazwa, cena in nazwy_lekcji.items():
            wartosc_z_html = request.form.get(nazwa)
            if wartosc_z_html and wartosc_z_html.strip():
                ilosc_lekcji = int(wartosc_z_html)
                if ilosc_lekcji > 0:
                    sumowanie += ilosc_lekcji * cena
                    szczegoly[nazwa] = ilosc_lekcji

        if sumowanie > 0:
            historia.append({
                'szczegoly': szczegoly,
                'suma': sumowanie
            })
            zapisz_historie(historia)
            wynik = f"Suma = {sumowanie:.2f} zł"

    # --- PRZYGOTOWANIE GOTOWYCH WIERSZY DLA JINJA ---
    wiersze_tabeli = []
    for index_wpisu, wpis in enumerate(historia, start=1):
        pierwszy_wiersz_wpisu = True

        for nazwa, ilosc in wpis['szczegoly'].items():
            wiersze_tabeli.append({
                'nr_wpisu': f"#{index_wpisu}" if pierwszy_wiersz_wpisu else "",
                'nazwa': nazwa,
                'ilosc': ilosc,
                'suma': f"{wpis['suma']:.2f} zł" if pierwszy_wiersz_wpisu else ""
            })
            pierwszy_wiersz_wpisu = False

    # Obliczamy sumę całkowitą ze wszystkich wpisów w historii
    laczna_suma = sum(wpis['suma'] for wpis in historia)

    return render_template(
        "index.html",
        wynik=wynik,
        wiersze_tabeli=wiersze_tabeli,
        laczna_suma=f"{laczna_suma:.2f} zł"
    )


if __name__ == '__main__':
    app.run(debug=True)