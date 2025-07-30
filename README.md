

source venv/bin/activate

pip install beautifulsoup4 lxml
pip install requests beautifulsoup4


python parse_mzk.py


download_mzk - pobiera dane ze strony mzk
parse_mzk - zamienia dane htm z pobranych plikow w miare czytelnego jsona
remove_empty - usuwa puste foldery lol
rozklad_przystanki - zamienia dane z rozklad zbiorczy na jsona z liniami dla kazdego przystanku

rozklad_zbiorczy.json - nr linii [przystanek[czas o ktorych sie zatrzymuje]]
przystanki_do_linii - nazwa przystanku [jakie linie sie na nim zatrzymuja]

dopasowanie.py - prototyp naszej aplikacji, bierze 2 przystanki i zwraca potencjalne trasy