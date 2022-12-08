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
u_up = 1
u_flat = 2
u_down = 4
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

# --- Google OR-Tools TSP solver ---
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

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

# --- store data for problem ---
data = {}
data['num_vehicles'] = 1
data['depot'] = 0
data['distance_matrix'] = time_matrix

manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
search_parameters.time_limit.seconds = 60
# search_parameters.log_search = True

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} seconds'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for runner:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route time: {} seconds\n'.format(route_distance)

def get_routes(solution, routing, manager):
  """Get vehicle routes from a solution and store them in an array."""
  # Get vehicle routes and store them in a two dimensional array whose
  # i,j entry is the jth location visited by vehicle i along its route.
  routes = []
  for route_nbr in range(routing.vehicles()):
    index = routing.Start(route_nbr)
    route = [manager.IndexToNode(index)]
    while not routing.IsEnd(index):
      index = solution.Value(routing.NextVar(index))
      route.append(manager.IndexToNode(index))
    routes.append(route)
  return routes

solution = routing.SolveWithParameters(search_parameters)
if solution:
    print_solution(manager, routing, solution)
routes = get_routes(solution, routing, manager)
# Display the routes.
route_points = []
for i, route in enumerate(routes):
    for j, m in enumerate(route):
        if j == 0:
            route_points.append(find_closest_coast(mountains[route[1]-1].a, mountains[route[1]-1].b))
        elif j == 61:
            route_points.append(find_closest_coast(mountains[route[59]-1].a, mountains[route[59]-1].b))
        else:
            route_points.append((mountains[m-1].a, mountains[m-1].b))
    print('Route', i, route)
    print(len(route_points), ' route points: ', route_points)
