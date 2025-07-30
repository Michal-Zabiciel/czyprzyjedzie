import os
import csv
from bs4 import BeautifulSoup
import re

def parse_html_file(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()

    print(f"\n[DEBUG] Plik: {filepath}")

    try:
        decoded = raw.decode('iso-8859-2')
    except UnicodeDecodeError:
        # awaryjnie spróbuj utf-8 (niektóre pliki mogą być tak zakodowane mimo meta)
        decoded = raw.decode('utf-8', errors='replace')

    soup = BeautifulSoup(decoded, 'lxml')

    tyt1 = soup.find('td', class_='tyt1')
    if not tyt1:
        print("❌ Nie znaleziono tyt1 (linia/przystanek/kierunek)")
        return []

    # Szukamy elementu <b> zawartego w przystanku:
    stop_name = "???"
    for elem in tyt1.descendants:
        if isinstance(elem, str) and 'przystanek:' in elem.lower():
            next_b = elem.find_next('b')  # szukamy <b> po "przystanek:"
            if next_b:
                stop_name = next_b.get_text(strip=True)
                break

    print(f"  Nazwa przystanku: {stop_name}")

    text = tyt1.get_text(" ", strip=True)

    # Extract linia number (e.g. "Linia 8" → 8)
    linia_match = re.search(r'Linia\s+(\d+)', text)
    linia_number = linia_match.group(1) if linia_match else "???"

    print(f"  Linia: {linia_number}")

    text = tyt1.get_text(" ", strip=True)

    # Kierunek
    kierunek_match = re.search(r'kierunek:\s*(.*)', text, re.IGNORECASE)
    kierunek = kierunek_match.group(1).strip() if kierunek_match else "???"

    print(f"  Kierunek: {kierunek}")




    # 2. Czy tyt2 istnieje i zawiera "robocze"
    tyt2 = soup.find('td', class_='tyt2')
    if not tyt2:
        print("❌ Nie znaleziono tyt2 (nagłówek z dniami tygodnia)")
        return []

    print(f"  tyt2: {tyt2.get_text(strip=True)}")

    if 'robocze' not in tyt2.get_text(strip=True).lower():
        print("❌ tyt2 nie zawiera słowa 'robocze'")
        return []
    
    tabela = tyt2.find_parent('table')
    rows = soup.find_all('tr',attrs= {"align":lambda val: val and val.lower() == "center"})
    # <TR ALIGN="CENTER">
    #print(f"  znaleziono {len(rows)} wierszy align=center")
    #print(f"Rows: {rows}")
        

    # w tym trybie nic nie zwracamy – to tylko podgląd
    # zwracamy godziny to nas interesuje
    godziny = []
    for i, row in enumerate(rows):
        if i == 2:
            godziny = ([td.get_text(strip=True) for td in row.find_all('td')])
        if i == 3:
            minuty = ([td.get_text(strip=True) for td in row.find_all('td')])

    czasy = []
    for i in range(len(godziny)):
        if (minuty[i] != "-"):
            #print(godziny[i])
            if len(minuty[i]) == 1:
                minuty[i] = "0" + minuty[i]
            if len(godziny[i]) == 1:
                godziny[i] = "0" + godziny[i]
            czasy.append(godziny[i].replace('.', '') + minuty[i].replace('.', ''))


    return {
        'linia': linia_number,
        'kierunek': kierunek,
        'przystanek': stop_name,
        'czasy': czasy
    }


def parse_all_html_in_folder(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.htm'):
            fullpath = os.path.join(folder_path, filename)
            fileData = parse_html_file(fullpath)  # np. ['0644', '1258', ...]

            if fileData:
                all_data.append(fileData)

    return all_data


from collections import defaultdict
import json

import unicodedata

def normalize(text):
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)

    # Ręczna naprawa błędnych znaków
    text = text.replace("ďż˝", "Ę")

    return text.strip()


def save_to_json(data, filename='rozkład.json'):
    grouped = {}

    for entry in data:
        linia = normalize(entry['linia'])
        kierunek = normalize(entry['kierunek'])
        key = (linia, kierunek)

        if key not in grouped:
            grouped[key] = {
                'linia': linia,
                'kierunek': kierunek,
                'stops': []
            }

        grouped[key]['stops'].append({
            'przystanek': normalize(entry['przystanek']),
            'czasy': entry['czasy']
        })

    # Convert dict to list
    json_data = list(grouped.values())

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)



    #folder = 'htm'  # katalog z plikami .htm
    #dane = parse_all_html_in_folder(folder)
    #dane.sort(key=lambda entry: int(entry['czasy'][0]))
    #save_to_json(dane)
def only_digits(s):
    return ''.join(c for c in s if c.isdigit())

def sort_key(entry):
    if entry['czasy']:
        cleaned = only_digits(entry['czasy'][0])
        if cleaned.isdigit():
            return int(cleaned)
    return 9999

if __name__ == '__main__':
    BASE_DIR = 'htm_all_linie'  # main folder containing linia_* subfolders
    all_dane = []

    for linia_folder in sorted(os.listdir(BASE_DIR)):
        subpath = os.path.join(BASE_DIR, linia_folder)
        if os.path.isdir(subpath):
            print(f"\nPrzetwarzanie folderu: {linia_folder}")
            dane = parse_all_html_in_folder(subpath)
            all_dane.extend(dane)

    # Sort all stops by earliest departure time
    all_dane.sort(key=sort_key)

    # Posortuj listę po polu 'linia' numerycznie
    all_dane.sort(key=lambda x: int(x['linia']) if x['linia'].isdigit() else 9999)



    print(f"\n  Łącznie odczytano {len(all_dane)} przystanków.")
    save_to_json(all_dane, filename='rozklad_zbiorczy.json')

