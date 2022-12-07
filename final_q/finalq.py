import math

alpha = 30

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

#print(find_abc(734))
#print(math.factorial(60))

class Mountain:
    def __init__(self, a, b, c):
        radius = (0.1875*c)/math.tan(alpha)
        self.a = a
        self.b = b
        h = 0.1875 * c
        invalid_dest = []

def is_below(mountain1, mountain2, alpha):
    dist = math.sqrt((math.abs(mountain1.a-mountain2.a))**2 + (math.abs(mountain1.b-mountain2.b)))
    if mountain2.h > mountain1.h:
        r1 = mountain2.radius
        minor_r = r1 - dist
        if minor_r <= 0:
            return False
        if mountain2.h * (minor_r/r1) > mountain1.h:
            return True
        return False
    else:
        r1 = mountain1.radius
        minor_r = r1 - dist
        if minor_r <= 0:
            return False
        if mountain1.h * (minor_r/r1) > mountain2.h:
            return True
        return False

mountains = []   
for mountain_data in find_abc(734):
    mountains.append(Mountain(mountain_data[0], mountain_data[1], mountain_data[2]))
print(mountains)
print(mountains[5].a)