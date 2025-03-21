def findPotentialPaths(start, end, data):
    #1 step one find directs
    paths = []
    for line in data:
        #print(line)
        if start in data[line] and end in data[line]:
            paths.append(line)

    return paths