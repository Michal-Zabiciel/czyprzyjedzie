def after(time1, time2):
    time1 = time1.strip()
    time2 = time2.strip()
    #print(f"Testujemy czy {time1} jest po {time2}")
    for y in range(4):
        if (time1[y] > time2[y]):
            #print("Tak")
            return True
        if (time1[y] < time2[y]):
            #print("Nie")
            return False
    #print(f"Nie")
    return False

def calculateDuration(startTime, endTime):
    godziny = ( int(endTime[0]) - int(startTime[0]) ) * 10 + ( int(endTime[1]) - int(startTime[1] ))
    minuty = ( int(endTime[2]) - int(startTime[2]) ) * 10 + ( int(endTime[3]) - int(startTime[3]) )
    czas = godziny * 60 + minuty
    return czas