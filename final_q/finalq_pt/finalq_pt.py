from itertools import combinations, permutations
from sys import maxsize

class circles:
    def __init__(self, x, y, height, radius):
        self.x = x
        self.y = y
        self.height = height
        self.radius = radius

circles_lst = []
for i in permutations([n ** 2 for n in range(28)], 3):
    if sum(i) == 734:
        circles_lst.append(
            circles(round(i[0] ** 0.5), round(i[1] ** 0.5), 0.1875 * round(i[2] ** 0.5), 0.25 * round(i[2] ** 0.5)))

class circles_pairs:
    def __init__(self, circle1, circle2, state, time):
        self.circle1 = circle1
        self.circle2 = circle2
        self.state = state
        self.time = time

circles_pairs_lst = []
for pairs in permutations(circles_lst, 2):  # P as time for A to B is not the same as B to A
    a = pairs[0]  # first circle
    b = pairs[1]  # second circle
    # externally touched: distance = r1 + r2
    if ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5 == a.radius + b.radius:
        circles_pairs_lst.append(circles_pairs(circles_lst.index(a), circles_lst.index(b), "externally touch", 0))
    # internally touched: distance = r1 - r2
    elif ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5 == abs(a.radius - b.radius):
        circles_pairs_lst.append(circles_pairs(circles_lst.index(a), circles_lst.index(b), "internally touch", 0))
    # not intersecting: distance > r1 + r2
    elif ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5 > a.radius + b.radius:
        circles_pairs_lst.append(circles_pairs(circles_lst.index(a), circles_lst.index(b), "no intersections", 0))
    # inside another circle: distance < r1 - r2
    elif ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5 < abs(a.radius - b.radius):
        circles_pairs_lst.append(circles_pairs(circles_lst.index(a), circles_lst.index(b), "one is inside", 0))
    # intersects at 2 points:
    else:
        circles_pairs_lst.append(circles_pairs(circles_lst.index(a), circles_lst.index(b), "2 intersections", 0))

# 0 pairs externally touch
# 0 pairs internally touch
# 2960 pairs don't intersect
# 12 pairs one is inside another (invalid)
# 568 pairs have 2 intersections

for pairs in circles_pairs_lst:
    A = circles_lst[pairs.circle1]
    B = circles_lst[pairs.circle2]
    if pairs.state == "no intersections":
        # A slope * 1000/4 + flat distance * 1000/2 + B slope * 1000/1 s
        d = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5
        pairs.time = (A.radius * 1000 / 4) + (d - A.radius - B.radius) * 1000 / 2 + (B.radius * 1000)
    elif pairs.state == "2 intersections":
        # top of A horizontal -> (distance + r0 - r1)/2 
        # top of B horizontal -> (distance + r1 - r0)/2 
        d = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5
        pairs.time = ((d + A.radius - B.radius) / 2 * 1000 / 4) + ((d + B.radius - A.radius) / 2 * 1000)

graph = []
for i in range(60):
    lst = []
    for moutain in circles_pairs_lst:
        if moutain.circle1 == i:
            lst.append(moutain.time)
    graph.append(lst)
for i in range(60):
    graph[i].insert(i, 0)
    

import numpy as np
from python_tsp.heuristics import solve_tsp_local_search

distance_matrix = np.array(graph)
order, duration = solve_tsp_local_search(distance_matrix)
# complete path of 60 moutains end at the starting point
# if starts at order[i], ends at order[i - 1]

def time_from_shore(x, y, r, start):
    lst = []
    for i in range(0, 28):
        lst.append([i, math.ceil((28**2 - i**2)**0.5)])
    for i in range(0, 28):
        if [math.ceil((28 ** 2 - i ** 2) ** 0.5), i] not in lst:
            lst.append([math.ceil((28 ** 2 - i ** 2) ** 0.5), i]) 
    
    distance_from_point = []
    for i in lst:
        distance_from_point.append(((i[0] - x)**2 + (i[1] - y)**2)**0.5)
    closest_point = lst[distance_from_point.index(min(distance_from_point))]
    
    if start == True:
        return (((closest_point[0] - x)**2 + (closest_point[1] - y)**2)**0.5 - r) * 1000 / 2 + r * 1000
    else:
        return (((closest_point[0] - x)**2 + (closest_point[1] - y)**2)**0.5 - r) * 1000 / 2 + r * 1000 / 4

# we need to remove time between end to start, and add duration from shore to start plus duration from end to shore

duration_difference = []
for k in range(60):
    start = circles_lst[order[k]]
    end = circles_lst[order[k - 1]]
    
    duration_from_end_to_start = 0
    for i in circles_pairs_lst:
        if i.circle1 == order[k - 1] and i.circle2 == order[k]:
            duration_from_end_to_start = i.time
            break;
    
    duration_difference.append(duration_from_end_to_start - time_from_shore(start.x, start.y, start.radius, True) - time_from_shore(end.x, end.y, end.radius, False))

    
print(order)
print(duration - max(duration_difference))


