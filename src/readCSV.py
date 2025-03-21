import csv
from typing import Dict,List

MyDictType = Dict[str, List[str]]

listaLinii = ["8-1", "11-1", "11-2", "1", "2"]


def readCSVs():
    data: MyDictType = {}
    for x in range(len(listaLinii)):
        with open(f'../schedules/{listaLinii[x]}.csv', mode = 'r') as file:
            linia = listaLinii[x]
            csvFile = csv.reader(file)
            rows = list(csvFile)
            for line in rows:
                if linia in data:
                    data[linia].append(line[0])
                else:
                    data[linia] = [line[0]]

    return data