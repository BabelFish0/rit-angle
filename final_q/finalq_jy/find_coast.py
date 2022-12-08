import math

global infin
global island_r
island_r = 28
infin = 1000000

def find_closest_coast(a, b):
    '''Return closest int valid coastal point to mountain coords (a, b).'''
    v = (a, b)
    lowest_dist = infin
    mag_v = math.sqrt(a**2+b**2)
    test = []

    if v == (0, 0):
        return (0, island_r)
    unit_v = tuple(n/mag_v for n in v)
    point = tuple(n*island_r for n in unit_v)

    if point[0] == int(point[0]) and point[1] == int(point[1]):
        return point
    for i in range(0, 4):
        x_comp = math.ceil(point[0])*(i % 2) + math.floor(point[0])*(1-(i % 2))
        y_comp = math.ceil(point[1])*(i // 2) + math.floor(point[1])*(1-(i // 2))
        test.append((x_comp, y_comp))
        dist = math.sqrt((x_comp - a)**2 + (y_comp - b)**2)
        if dist < lowest_dist and math.sqrt(x_comp**2 + y_comp**2) < island_r:
            lowest_dist = dist
            best_int_point = (x_comp, y_comp)
    return best_int_point
    print(lowest_dist, best_int_point, test)


print(find_closest_coast(10, 15))
print(find_closest_coast(0, 0))
print(find_closest_coast(0, 28))