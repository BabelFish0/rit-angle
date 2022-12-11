import math
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np

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

class Mountain:
    def __init__(self, a, b, c):
        self.radius = (0.1875*c)/math.tan(alpha)
        self.a = a
        self.b = b
        self.h = 0.1875 * c
        self.invalid_dest = []

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

# --- initialize mountains ---
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
        return 0 #testing CHANGE TO INFIN
    if mountain1 == mountain2:
        return 0
    d = dist(mountain1, mountain2)
    if d >= mountain1.radius + mountain2.radius:
        return mountain1.radius / u_down + (d - mountain1.radius - mountain2.radius) / u_flat + mountain2.radius / u_up
    d1 = (mountain1.h - mountain2.h + gradient*d)/(2*gradient)
    d2 = d - d1
    return d1 / u_down + d2 / u_up

def find_closest_coast(a, b):
    '''Return closest int valid coastal point to mountain coords (a, b).'''
    v = (a, b)
    lowest_dist = infin
    mag_v = math.sqrt(a**2+b**2)

    if v == (0, 0):
        return (0, island_r)
    unit_v = tuple(n/mag_v for n in v)
    point = tuple(n*island_r for n in unit_v)

    if point[0] == int(point[0]) and point[1] == int(point[1]):
        return point
    for i in range(0, 4):
        x_comp = math.ceil(point[0])*(i % 2) + math.floor(point[0])*(1-(i % 2))
        y_comp = math.ceil(point[1])*(i // 2) + math.floor(point[1])*(1-(i // 2))
        dist = math.sqrt((x_comp - a)**2 + (y_comp - b)**2)
        if dist < lowest_dist and math.sqrt(x_comp**2 + y_comp**2) >= island_r: #check inequality
            lowest_dist = dist
            best_int_point = (x_comp, y_comp)
    return best_int_point

def time_coast(m, towards_coast=True):
    '''
    Return time in s FROM mountain m TO nearest coast (towards_coast True)
    Return time in s FROM nearest coast TO mountain m (towards_coast False)
    '''
    point = find_closest_coast(m.a, m.b)
    flat_dist = math.sqrt((m.a-point[0])**2 + (m.b-point[1])**2) - m.radius #note: no mountains go over coast
    if towards_coast:
        return m.radius / u_down + flat_dist / u_flat
    return m.radius / u_up + flat_dist / u_flat

# --- create time data ---
matrix_scaling = 1000
time_matrix = np.zeros((61, 61), dtype=int)
for i in range(1, np.shape(time_matrix)[0]):
    for j in range(1, np.shape(time_matrix)[1]):
        time_matrix[i][j] = int(matrix_scaling * time(mountains[i-1], mountains[j-1])) #check i, j order
        # if time_matrix[i][j] < 0: #checking for illegal times
        #     print(time_matrix[i][j], i, j, (mountains[i-1].a, mountains[i-1].b, mountains[i-1].h, mountains[i-1].radius), (mountains[j-1].a, mountains[j-1].b, mountains[j-1].h, mountains[j-1].radius))

for j in range(1, np.shape(time_matrix)[0]): #coast to mountain
    time_matrix[0][j] = int(matrix_scaling * time_coast(mountains[j-1], False))

for i in range(1, np.shape(time_matrix)[0]): #mountain to coast
    time_matrix[i][0] = int(matrix_scaling * time_coast(mountains[i-1], True))
np.set_printoptions(threshold=np.inf)
#print(time_matrix)

import numpy as np
from python_tsp.heuristics import solve_tsp_local_search

permutation, distance = solve_tsp_local_search(time_matrix)
print(permutation, '\n' , distance/matrix_scaling)