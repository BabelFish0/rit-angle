import math
import matplotlib.pyplot as plt
import matplotlib.patches as pat

alpha = math.atan(3/4)
global infin
global u_up
global u_flat
global u_down
infin = 10000000000000
u_up = 1
u_flat = 2
u_down = 4
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
print(mountains[5].invalid_dest)


# --- Google OR-Tools TSP solver ---
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def dist(m1, m2):
    return math.sqrt((m1.a-m2.a)**2 + (m1.b-m2.b)**2)

def time(mountain1, mountain2):
    '''Return time in s FROM mountain1 TO mountain2.'''
    if mountain2 in mountain1.invalid_dest:
        return infin
    d = dist(mountain1, mountain2)
    if d > mountain1.radius + mountain2.radius:
        return mountain1.radius / u_down + (d - mountain1.radius - mountain2.radius) / u_flat + mountain2.radius / u_up
    d1 = mountain1.radius * ((mountain2.radius**2-mountain1.radius**2-d**2)/(-2*mountain2.radius*d))
    d2 = mountain2.radius * ((mountain1.radius**2-mountain2.radius**2-d**2)/(-2*mountain1.radius*d))
    return d1 / u_down + d2 / u_up

def find_closest_coast(m):
    '''Return closest int valid coastal point to mountain m.'''
    # reminder: solve for point of coastal intersection. check lowest distance with all valid integer points in square around point in question.

# def create_data_model():
#     """Stores the data for the problem."""
#     data = {}
#     data['distance_matrix'] = [