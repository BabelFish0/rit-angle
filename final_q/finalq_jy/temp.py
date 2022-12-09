# l = [0, 60, 59, 57, 55, 51, 45, 47, 52, 58, 56, 48, 43, 39, 40, 36, 28, 27, 33, 35, 31, 23, 17, 3, 1, 7, 8, 9, 4, 13, 15, 21, 25, 26, 18, 19, 22, 16, 14, 5, 10, 11, 12, 2, 6, 20, 24, 29, 30, 32, 34, 38, 42, 37, 41, 44, 46, 50, 49, 53, 54, 0]
# for i in range(0, 62):
#     if i not in l:
#         print(i)

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
        return infin
    if mountain1 == mountain2:
        return 0
    d = dist(mountain1, mountain2)
    if d >= mountain1.radius + mountain2.radius:
        return mountain1.radius / u_down + (d - mountain1.radius - mountain2.radius) / u_flat + mountain2.radius / u_up
    d1 = (mountain1.h - mountain2.h + gradient*d)/(2*gradient)
    d2 = d - d1
    return d1 / u_down + d2 / u_up

coord = []
for mountain in mountains:
    coord.append((mountain.a, mountain.b))

print(coord)

print(time(mountains[0], mountains[6]))