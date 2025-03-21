import csv
from readCSV import readCSVs
from support import calculateDuration, after
from potentialPaths import findPotentialPaths


listaLinii = ["8-1", "11-1", "11-2", "1", "2"]



def scanRoute(rows, end):
    print("scanning route")

mypath = readCSVs()
print(mypath["8-1"])

start = "Start"#"Wyszynskiego - Policja"
end = "End"#"Szczebrzeska - Zoo"
#end = "Wyszynskiego - Policja"
#start = "Szczebrzeska - Zoo"
startTime = "0616"
time_before = "0520"
time_after = "1020"


paths = findPotentialPaths(start, end, mypath)
print(paths)

print(f"Wyruszasz na podroz z {start} do {end} o godzinie {startTime}")
print(f"Obecny filtr znajduje trase ktora dojedziesz najszybciej")



shortestArrivalTime = "2137"
koncowaLinia = "Swinia"
startIndex = -1
endIndex = -1
journeyTime = -1
finalStartTime = "2137"

'''for x in range(len(listaLinii)):
    with open(f'../schedules/{listaLinii[x]}.csv', mode = 'r') as file:
        linia = listaLinii[x]
        #print(f"Testujemy linie {linia}")
        csvFile = csv.reader(file)
        startIndex = -1
        endIndex = -1
        index = 0
        rows = list(csvFile)
        for line in rows:
            if (line[0] == start):
                startIndex = index

            if (line[0] == end and startIndex != -1):
                endIndex = index
            index = index + 1
        #print(f"{rows[startIndex][0]} and {rows[endIndex][0]}")

        if (startIndex == -1 and endIndex == -1):
            #print(f"Nie znaleziono trasy dla tej linii: {linia}")
            continue
        elif (startIndex != -1):
            scanRoute(rows, end)
            continue

        iterationOfBus = -1

        for x in range(1, len(rows[startIndex])):
            #print(x)
            if after(rows[startIndex][x], startTime):
                #print(f"Bedziesz jechal {x} autobusem tego dnia")
                iterationOfBus = x
                break

        startTime = rows[startIndex][iterationOfBus].strip()
        endTime = rows[endIndex][iterationOfBus].strip()

        journeyTime = calculateDuration(startTime, endTime)

        print(f"Mozliwa trasa: linia {linia}, godzina {startTime}, dojazd o {endTime}. Podroz potrwa {journeyTime} minut")


        if after(shortestArrivalTime, endTime):
            shortestArrivalTime = endTime
            koncowaLinia = linia
            finalStartTime = startTime

print(f"Wsiadziesz w autobus linii {koncowaLinia}, o godzinie {finalStartTime} i dojedziesz na miejsce o godzinie {shortestArrivalTime}. Podroz potrwa {journeyTime} minut")
'''
