import math
import matplotlib.pyplot as plt
import matplotlib.patches as pat

alpha = math.atan(3/4)

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

