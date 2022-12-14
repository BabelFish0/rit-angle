import math

alpha = math.atan(3/4)
global gradient
gradient = 3/4

global infin
global u_up
global u_flat
global u_down
global island_r
infin = 100000
u_up = 0.001 #km/s
u_flat = 0.002
u_down = 0.004
island_r = 28
coast = []

def test_integer(a, b, c, n):
    return a**2 + b**2 + c**2 == n

def find_abc(n):
    out = []
    for a in range(int(math.sqrt(n))+1):
        for b in range(int(math.sqrt(n))+1):
            for c in range(int(math.sqrt(n))+1):
                if test_integer(a, b, c, n):
                    out.append([a, b, c])
    return out

def query_covers(mountain1, mountain2, alpha):
    '''
    input: mountain1, Mountain object
    mountain2, Mountain object
    alpha, angle of slope (rad)
    returns: True/False for does mountain1 cover mountain2 or mountain2 cover mountain1?
    '''
    dist = math.sqrt((abs(mountain1.a - mountain2.a))**2 +
	                 (abs(mountain1.b - mountain2.b))**2)
    if mountain2.h > mountain1.h:
        r1 = mountain2.radius
        if mountain1.radius + dist < r1:
            return True
        return False
    else:
        r1 = mountain1.radius
        if mountain2.radius + dist < r1:
            return True
        return False

class Mountain:
    def __init__(self, a, b, c):
        self.radius = (0.1875*c)/math.tan(alpha)
        self.a = a
        self.b = b
        self.h = 0.1875 * c
        self.invalid_dest = []

mountains = []
for mountain_data in find_abc(734):
    mountains.append(Mountain(mountain_data[0], mountain_data[1], mountain_data[2]))

# --- identify impossible journeys for each mountain ---
for mountain1 in mountains:
    for mountain2 in mountains:
        if query_covers(mountain1, mountain2, alpha) and mountain1 != mountain2:
            mountain1.invalid_dest.append(mountain2)

def dist(m1, m2):
    return math.sqrt((m1.a-m2.a)**2 + (m1.b-m2.b)**2)

def time(mountain1, mountain2):
    '''Return time in s FROM mountain1 TO mountain2.'''
    if mountain2 in mountain1.invalid_dest or mountain1 in mountain2.invalid_dest:
        return infin
    d = dist(mountain1, mountain2)
    if d >= mountain1.radius + mountain2.radius:
        return mountain1.radius / u_down + (d - mountain1.radius - mountain2.radius) / u_flat + mountain2.radius / u_up
    d1 = (mountain1.h - mountain2.h + gradient*d)/(2*gradient)
    d2 = d - d1
    return d1 / u_down + d2 / u_up

def time_coast(coast, m, towards_coast=True):
    '''
    Return time in s FROM mountain m TO nearest coast (towards_coast True)
    Return time in s FROM nearest coast TO mountain m (towards_coast False)
    '''
    flat_dist = math.sqrt((m.a-coast[0])**2 + (m.b-coast[1])**2) - m.radius #note: no mountains go over coast
    if towards_coast:
        return m.radius / u_down + flat_dist / u_flat
    return m.radius / u_up + flat_dist / u_flat

t = 0
ordered_mountain_points = []
for mountain in mountains:
    ordered_mountain_points.append((mountain.a, mountain.b))
# points = [(2, 28), (2, 27), (1, 27), (3, 26), (3, 25), (3, 23), (2, 21), (5, 22), (6, 23), (7, 26), (10, 25), (9, 22), (7, 19), (7, 18), (11, 18), (11, 17), (9, 13), (6, 13), (5, 15), (2, 17), (3, 14), (3, 10), (3, 7), (1, 2), (2, 1), (7, 3), (10, 3), (14, 3), (17, 2), (15, 5), (13, 6), (13, 9), (17, 11), (18, 11), (18, 7), (19, 7), (22, 9), (23, 6), (22, 5), (21, 2), (23, 3), (25, 3), (26, 3), (27, 1), (27, 2), (26, 7), (25, 10), (22, 13), (23, 13), (23, 14), (22, 15), (21, 17), (19, 18), (18, 17), (17, 18), (18, 19), (17, 21), (15, 22), (13, 22), (13, 23), (14, 23), (15, 24)]
# test = [0, 6, 2, 12, 11, 10, 5, 14, 16, 20, 24, 22, 19, 18, 26, 25, 21, 15, 13, 4, 9, 8, 7, 1, 3, 17, 23, 31, 35, 33, 27, 28, 36, 40, 39, 43, 48, 52, 47, 45, 51, 55, 57, 59, 60, 58, 56, 49, 53, 54, 50, 46, 44, 41, 37, 42, 38, 34, 29, 30, 32, 0]
# for i, m_index in enumerate(test):
#     if i == 0:
#         t += time_coast(points[i], mountains[test[i+1]-1], towards_coast=False)
#     elif i == 60:
#         t += time_coast(points[i+1], mountains[test[i]-1], towards_coast=True)
#     elif i == 61:
#         t = t
#     else:
#         t += time(mountains[m_index-1], mountains[test[i+1]-1])
# print(t)

# test = [(28,1),(27,1),(27,2),(26,3),(25,3),(23,3),(21,2),(22,5),(23,6),(19,7),(18,7),(18,11),(17,11),(13,9),(13,6),(15,5),(17,2),(14,3),(10,3),(7,3),(2,1),(1,2),(3,7),(3,10),(3,14),(2,17),(2,21),(5,22),(7,19),(7,18),(5,15),(6,13),(9,13),(11,17),(11,18),(9,22),(6,23),(3,23),(1,27),(2,27),(3,25),(3,26),(7,26),(10,25),(14,23),(13,22),(13,23),(15,22),(17,21),(18,19),(17,18),(18,17),(19,18),(21,17),(22,15),(23,13),(23,14),(22,13),(22,9),(25,10),(26,7),(27,8)]
# for i, point in enumerate(test):
#     if i == 0:
#         t += time_coast(point, mountains[ordered_mountain_points.index(test[i+1])], towards_coast=False)
#     elif i == 60:
#         t += time_coast(test[i+1], mountains[ordered_mountain_points.index(point)], towards_coast=True)
#     elif i == 61:
#         t = t
#     else:
#         t += time(mountains[ordered_mountain_points.index(point)], mountains[ordered_mountain_points.index(test[i+1])])
# print(t)

# test = [(2,28),(2,27),(1,27),(3,26),(3,25),(3,23),(2,21),(5,22),(6,23),(7,26),(10,25),(9,22),(7,19),(7,18),(11,18),(11,17),(9,13),(6,13),(5,15),(2,17),(3,14),(3,10),(3,7),(1,2),(2,1),(7,3),(10,3),(14,3),(17,2),(15,5),(13,6),(13,9),(17,11),(18,11),(18,7),(19,7),(22,9),(23,6),(22,5),(21,2),(23,3),(25,3),(26,3),(27,1),(27,2),(26,7),(25,10),(22,13),(23,13),(23,14),(22,15),(21,17),(19,18),(18,17),(17,18),(18,19),(17,21),(15,22),(13,22),(13,23),(14,23),(15,24)]
# for i, point in enumerate(test): #current second best
#     if i == 0:
#         t += time_coast(point, mountains[ordered_mountain_points.index(test[i+1])], towards_coast=False)
#     elif i == 60:
#         t += time_coast(test[i+1], mountains[ordered_mountain_points.index(point)], towards_coast=True)
#     elif i == 61:
#         t = t
#     else:
#         t += time(mountains[ordered_mountain_points.index(point)], mountains[ordered_mountain_points.index(test[i+1])])
# print(t)

test = [(1, 28), (1, 27), (2, 27), (3, 26), (3, 25), (3, 23), (2, 21), (5, 22), (6, 23), (9, 22), (7, 19), (7, 18), (11, 18), (11, 17), (9, 13), (6, 13), (5, 15), (2, 17), (3, 14), (3, 10), (3, 7), (1, 2), (2, 1), (7, 3), (10, 3), (14, 3), (17, 2), (15, 5), (13, 6), (13, 9), (17, 11), (18, 11), (18, 7), (19, 7), (22, 9), (23, 6), (22, 5), (21, 2), (23, 3), (25, 3), (27, 1), (27, 2), (26, 3), (26, 7), (25, 10), (23, 13), (23, 14), (22, 13), (22, 15), (21, 17), (19, 18), (18, 17), (17, 18), (18, 19), (17, 21), (15, 22), (14, 23), (13, 22), (13, 23), (10, 25), (7, 26), (8, 27)]
for i, point in enumerate(test): #current best
    if i == 0:
        t += time_coast(point, mountains[ordered_mountain_points.index(test[i+1])], towards_coast=False)
    elif i == 60:
        t += time_coast(test[i+1], mountains[ordered_mountain_points.index(point)], towards_coast=True)
    elif i == 61:
        t = t
    else:
        t += time(mountains[ordered_mountain_points.index(point)], mountains[ordered_mountain_points.index(test[i+1])])
print(t)