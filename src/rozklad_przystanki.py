import json
from collections import defaultdict

def normalize(text):
    return text.strip() if text else ""

# Wczytaj dane z pliku
with open('rozklad_zbiorczy.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Tworzymy słownik: przystanek → set(linii)
stops_to_lines = defaultdict(set)

for entry in data:
    linia = normalize(entry['linia'])

    for stop in entry['stops']:
        przystanek = normalize(stop['przystanek'])
        stops_to_lines[przystanek].add(linia)

# Zamień zbiory na listy i ewentualnie posortuj
result = {
    stop: sorted(list(lines), key=lambda x: int(x) if x.isdigit() else x)
    for stop, lines in stops_to_lines.items()
}

# Zapisz do pliku
with open('przystanki_do_linii.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("  Gotowe: utworzono mapę przystanków do linii.")