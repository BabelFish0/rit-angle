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
    if pairs.state == "no intersections":
        # height, radius, slope is a 3,4,5 right triangle
        # A slope * 1000/4 + flat distance * 1000/2 + B slope * 1000/1 s
        A = circles_lst[pairs.circle1]
        B = circles_lst[pairs.circle2]
        pairs.time = (A.radius * 5 / 4 * 1000 / 4) + ((((A.x - B.x)**2 + (A.y - B.y)**2) ** 0.5) - A.radius - B.radius)/2 + (B.radius * 5 / 4 * 1000)
    elif pairs.state == "2 intersections":
        # top of A slope -> (distance + r0 - r1)/2 * 5 / 4
        # top of B slope -> (distance + r1 - r0)/2 * 5 / 4
        A = circles_lst[pairs.circle1]
        B = circles_lst[pairs.circle2]
        d = ((A.x - B.x)**2 + (A.y - B.y)**2)**0.5
        pairs.time = ((d + A.radius - B.radius) / 2 * 5 / 4 * 1000 / 4) + ((d + B.radius - A.radius) / 2 * 5 / 4 * 1000)

graph = []
for i in range(60):
    lst = []
    for j in range(60):
        if i == j:
            lst.append(0)
        else:
            for k in circles_pairs_lst:
                if k.circle1 == i and k.circle2 == j:
                    lst.append(k.time)
    graph.append(lst)

def travellingSalesmanProblem(graph, s):
    # store all vertex apart from source vertex
    vertex = []
    for i in range(60):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation = permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]

        # update minimum
        min_path = min(min_path, current_pathweight)

    return min_path


s = 0
print(travellingSalesmanProblem(graph, s))
