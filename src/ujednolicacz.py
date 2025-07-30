import json

# Wczytaj stary format
with open("rozklad_zbiorczy.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Nowy format: linia → lista kierunków z przystankami
lines_to_stops = {}
for entry in raw_data:
    line = entry["linia"]
    if line not in lines_to_stops:
        lines_to_stops[line] = []
    lines_to_stops[line].append({
        "kierunek": entry["kierunek"],
        "stops": entry["stops"]
    })

# Zapisz nowy plik
with open("linie_do_kierunkow.json", "w", encoding="utf-8") as f:
    json.dump(lines_to_stops, f, ensure_ascii=False, indent=2)

print("Zapisano nowy plik: linie_do_kierunkow.json")