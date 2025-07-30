import json
import difflib
import unicodedata
from support import calculateDuration, after

def normalize(text):
    # Normalizacja do ASCII bez znaków diakrytycznych + małe litery
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    ).lower()

# Wczytanie mapy przystanek -> linie
with open('przystanki_do_linii.json', 'r', encoding='utf-8') as f:
    stops_to_lines = json.load(f)

# Wczytanie mapy linia - przystanki
with open('linie_do_kierunkow.json', 'r', encoding='utf-8') as f:
    linie_do_kierunkow = json.load(f)

# Mapa uproszczona: bez polskich znaków → oryginał
normalized_to_original = {}
for stop in stops_to_lines.keys():
    norm = normalize(stop)
    normalized_to_original[norm] = stop

# Lista nazw uproszczonych
normalized_names = list(normalized_to_original.keys())

def find_best_match(user_input, limit=5):
    normalized_input = normalize(user_input)
    matches = difflib.get_close_matches(normalized_input, normalized_names, n=limit, cutoff=0.4)
    return [normalized_to_original[m] for m in matches]

def choose_stop(prompt):
    while True:
        user_input = input(prompt).strip()
        matches = find_best_match(user_input)

        if not matches:
            print("Nie znaleziono podobnych przystanków. Spróbuj ponownie.")
            continue

        print("Czy chodziło Ci o:")
        for i, name in enumerate(matches):
            print(f"{i + 1}. {name}")

        choice = input("Wybierz numer lub wpisz ponownie: ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(matches):
                return matches[index]
        else:
            # Spróbuj z nowym tekstem
            continue

def calculatePathOnLine(start, end, line, time):
    directions = linie_do_kierunkow[line]

    for direction in directions:
        #print(direction["stops"])
        pierwszy = False
        drugi = False
        trasa = []
        for stop in direction["stops"]:
            nazwa = stop["przystanek"]
            #print(nazwa)
            
            if nazwa == start:
                pierwszy = True
                czasy = stop["czasy"]
                for czas in czasy:
                    if after(czas, time):
                        czas_odjazdu = czas
                        break
            if nazwa == end: 
                drugi = True
                czasy = stop["czasy"]
                for czas in czasy:
                    if after(czas, time):
                        czas_dojazdu = czas
                        break

            if pierwszy:
                trasa.append(nazwa)
                #print(trasa)
            
            if drugi and not pierwszy:
                break

            if pierwszy and drugi:
                
                kierunek = direction["kierunek"]
                return {
                    "kierunek": kierunek,
                    "czas_odjazdu": czas_odjazdu,
                    "czas_przyjazdu": czas_dojazdu,
                    "trasa": trasa
                }
                break
            
    return {
        "kierunek": kierunek,
        "czas_odjazdu": czas_odjazdu,
        "czas_przyjazdu": czas_dojazdu,
        "trasa": trasa
    }
            #print(f"- {nazwa}: {czasy}")

# Program główny
print("Szukanie trasy pomiędzy przystankami")
start = "WYSZYŃSKIEGO NR 176,177 [RONDO]" #choose_stop("Podaj nazwę przystanku początkowego: ")
end = "AKADEMICKA- KR.JADWIGI NR 38,60" #choose_stop("Podaj nazwę przystanku końcowego: ")
time = "1420" #input("Podaj godzine w formacie: 1420 (czternasta dwadziescia)").strip()

print(f"\n Szukamy trasy z **{start}** do **{end}**...")


print(f"Linie obslugujace {start} to {stops_to_lines[start]}")
print(f"Linie obslugujace {end} to {stops_to_lines[end]}")

for line in stops_to_lines[start]:
    if line in stops_to_lines[end]:
        print(f"Szukamy trasy dla: {line}")
        info = calculatePathOnLine(start, end, line, time)
        print(f"Kierunek: {info["kierunek"]}, czas odjazdu: {info["czas_odjazdu"]}, czas przyjazdu: {info["czas_przyjazdu"]}, trasa: {info["trasa"]}")


    