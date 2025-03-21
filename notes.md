we need a way to store the paths between nodes

x0Y0 - x2y3

lets see what paths have x0y0

lets say we have directory with touples

{"8-1", [x0y0, x1y0, ...]}
{"8-2", [x0y0, x1y0, ...]}

or we could store full objects so
{"8-1", [{x0y0, 832, 954..}, x1y0, ...]}
{"8-2", [x0y0, x1y0, ...]}


1. we need to identify starting points, so all the lines that contain x0y0

2a. and end points, so all the lines that contain x2y3 maybe

2b. or if the starting point contains end stop

dijkstra maybe? but he is concerned about distance not time, 

3. if we have line {"8-1", [x0y0, x1y0, ...]} we can do the calculations

x0y0 - already starting point
x1y0 - find all the lines going from x1y0 so eg

{"11-1", [x1y0, x1y1, x2y3]}
{"11-2", [x1y0, x1y1, ...]}

4a. if a line goes to end point, bingo, so 11-1 for example. We then calculate path 8-1 and 11-1 combined.
4b. if a line does not go to the end point go to the next stop and check more paths so

{"11-2", [x1y0, x1y1, ...]}

repeat step 3 for x1y1 (next stop)




Potential scenarios:

1. Direct line - you can get to destination directly by bus from your starting point
2. You have to change once, you go to checkpoint and continue to goal
3. You have to change twice, you take a snake path, described in example
4. You can change, there is a direct path but its not really fast (eg. many stops). Real life scenario includes driving from second zone to a park and ride where you change from bus stopping everywhere into the tram that does the same path but faster.

Rejected scenarios:
1. More than two changes, this scenario would make the network two complex for my current skills and progress of the project. Ideally i want to create an algorithm capable of full recursion so this wont be a problem in the future. 