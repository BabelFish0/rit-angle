# Ritangle Final Question

### Jude Young

This document provides an overview to our approach for solving the final Ritangle 2022 question. The solution was programmed in Python. First, a brute force function for the generation of the mountains:
```py
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
```
The mountains are initialized with the list of [[a1, b1, c1], [a2, b2, c2], ...] from the above function as follows:
```py
class Mountain:
    def __init__(self, a, b, c):
        self.radius = (0.1875*c)/math.tan(alpha)
        self.a = a
        self.b = b
        self.h = 0.1875 * c
        self.invalid_dest = []

# --- initialize mountains ---
mountains = []
for mountain_data in find_abc(734):
    mountains.append(Mountain(mountain_data[0], mountain_data[1], mountain_data[2]))
```
Then, the internal list of invalid mountains is populated using the `query_covers` function which returns `True` if either of the mountains cover each other (and are unreachable). The function uses the fact that the cones of each mountain are similar and therefore if the radius of one of the moutains extends beyound the radius of the base of the other, it cannot be covered by it.
```py
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

# --- identify impossible journeys for each mountain ---
for mountain1 in mountains:
    for mountain2 in mountains:
        if query_covers(mountain1, mountain2, alpha) and mountain1 != mountain2:
            mountain1.invalid_dest.append(mountain2)
```
There are two situations for calculating the time of a leg of the journey: either it is between two mountains or a mountain and the nearest point to that mountain from the coast. For the first the `time` function is used:
```py
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
```
This function considers the case where flat land lies between the mountains (so the horizontal journey is just the two radii and the (distance between centres - the two radii)). If the mountains intersect, it solves for the horizontal distance from the centres of each of the mountains to the point of intersection in the vertical plane of the runner's journey. If the moutains are unreachable from each other, it returns `infin`, a global variable which is an effective infinite weight. `u_down`, `u_flat` and `u_up` are the horizontal speeds (global variables) for descending, traversing the flat land and ascending respectively.

Between a given mountain and the coast the program first finds the closest integer point beyond 28km from (0, 0):
```py
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
        x_comp = math.ceil(point[0])*(i % 2) + math.floor(point[0])*(1-(i % 2)) #cycle between ceiling and floor
        y_comp = math.ceil(point[1])*(i // 2) + math.floor(point[1])*(1-(i // 2)) #cycle between ceiling and floor (switches after i>=2)
        dist = math.sqrt((x_comp - a)**2 + (y_comp - b)**2)
        if dist < lowest_dist and math.sqrt(x_comp**2 + y_comp**2) >= island_r:
            lowest_dist = dist
            best_int_point = (x_comp, y_comp)
    return best_int_point
```
It first calculates the ideal (float) point on the circle of the coastline by calculating the unit vector towards the centre of the mountain in question and multiplying it by `island_r`, a global variable defining the radius of the island (28). This produces the tuple `point` (x, y). Then, the program generates the four integer points around the `point` (unless `point` is integer), alternating `floor` and `ceil` (ceiling) on the x and y components of `point`. It finds which one satisfies the condition of being outside `island_r` and has the lowest distance to the mountain and returns it as `best_int_point`.

The next function uses this to calculate the quickest time to/from the coast of a given mountain:
```py
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
```
If `towards_coast` is `True`, the downwards speed is used, as the journey consists of going down the mountain and across the flat plain; if `towards_coast` is `False`, the upwards speed is used.

