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

#print(find_abc(734))
#print(math.factorial(60))

class Mountain:
    def __init__(self, a, b, c):
        self.radius = (0.1875*c)/math.tan(alpha)
        self.a = a
        self.b = b
        self.h = 0.1875 * c
        self.invalid_dest = []

def is_below(mountain1, mountain2, alpha):
    dist = math.sqrt((abs(mountain1.a-mountain2.a))**2 + (abs(mountain1.b-mountain2.b))**2)
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
#print(mountains)
#print(mountains[5].a)

for mountain1 in mountains:
    for mountain2 in mountains:
        if is_below(mountain1, mountain2, alpha) and mountain1 != mountain2:
            mountain1.invalid_dest.append(mountain2)
#for i in range(len(mountains)):
 #   print(mountains[i].invalid_dest)

x = []
y = []
r = []
for mountain in mountains:
    x.append(mountain.a)
    y.append(mountain.b)
    r.append(mountain.radius)

fig, ax = plt.subplots()
plot = plt.plot(x, y, 'bx')
cc = []
for i in range(len(r)):
    cc.append(plt.Circle((x[i], y[i]), r[i]))
plt.show()

print(x, y, r)