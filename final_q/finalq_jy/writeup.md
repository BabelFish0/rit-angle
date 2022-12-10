# Ritangle Final Question

### Jude Young

This document provides an overview to our approach for solving the final Ritangle 2022 question. The solution was programmed in Python.

### Problem

Welcome to the fantasy island of Volcania!

Volcania is roughly the north-east quadrant of a circle. Its national grid, measured in kilometres, has $x=0$ along its western edge and $y=0$ on its southern edge. These two shorelines are mostly high cliffs. The NE shoreline is roughly circular. The sea reaches every whole-kilometre grid point that is 28 km or more from the SW corner, and no grid points that are closer than 28 km to the corner.

Volcania takes its name from its magical conical mountains. The mountains have their summits on the kilometre grid points $(a,b)$ and have height $0.1875c$ km above sea level, where $a, b$ and $c$ are each of the possible sets of positive integers that satisfy $a^2+b^2+c^2=734$. Each mountain is steep, with a constant gradient; lava always has the same viscosity and thermal properties, so all slopes make an equal angle $\alpha$ with the horizontal.

There is a flat coastal plain, at zero altitude, between the NE shoreline and the mountains.

Sabrina is a runner who wishes to visit each of the summits in the shortest possible time (no peak can be visited twice). She arrives by boat and lands at one of the grid points on the NE shore. She then visits each summit in turn before returning to a grid point on the NE shore (possibly the starting point but not necessarily). The magic of the island means that once she has picked her next destination, the other mountains (apart from one she is standing on, if any) all dematerialise. Her route will generally be directly down until she meets the slope up to the next target mountain, then directly up that mountain to its summit, where she chooses her next target. Nowhere on the island is below sea level; if Sabrina reaches flat ground at any point, she runs straight across it heading for her next chosen mountain.

If Sabrina chooses a ‘next mountain’ that is so high and so close to her that she is below ground level when it materialises, she will be buried alive. She would like to avoid this fate. Similarly, she cannot choose as her next target a mountain for which the summit is below the surface of her current mountain.

Sabrina’s speed across the map (i.e. the horizontal component of her speed over the ground surface) is $u=2(\tan\beta(1+\cos2\theta)+\sin2\theta)ms^{-1}$.

The angle $\theta$ is in Sabrina’s control (it depends on her running style). She picks different values for $\theta$ for running uphill, downhill and on the flat, so as to maximise her speed across the map at every stage. 

The angle $\beta$ is the angle to the horizontal at which she is running (so this is either $0, \alpha$ or $-\alpha$).

It transpires that Sabrina’s downhill speed (constant) is exactly four times her uphill speed (also constant).

Your task is to advise Sabrina at which grid point on the shoreline she should start, which order to tackle the mountains, and at which grid point she should finish. To support your advice you will need to calculate the total time taken for your best route in seconds.

Submit your answer in comma-separated format as follows:

Time taken to complete the route (in seconds, to 2 decimal places)

$(x, y)$ coordinates of start point (whole kilometres)

$(x, y)$ coordinates of each mountain visited (whole kilometres, in the order that Sabrina runs them)

$(x, y)$ coordinates of finish point (whole kilometres)

For example:\
123456.78\
28,0\
1,2\
2,3\
…\
0,28

### Solution

First, a brute force function for the generation of the mountains:
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

These functions are used to create the matrix `time_matrix` in which the (`i`, `j`) entry represents the time from mountain (`i-1`) to mountain (`j-1`). The shape of the matrix is (61, 61) because row 0 and column 0 represent the shortest time from the coast to each mountain and the time to the coast from each mountain respectively. Therefore, the index of a given mountain in `mountains` is one less than its index in `time_matrix`. It should also be noted that the solver only takes integer times, so a `matrix_scaling` factor of 1000 is applied to the timing matrix.
```py
# --- create time data ---
matrix_scaling = 1000
time_matrix = np.zeros((61, 61), dtype=int)
for i in range(1, np.shape(time_matrix)[0]): #mountain i-1 to mountain j-1
    for j in range(1, np.shape(time_matrix)[1]):
        time_matrix[i][j] = int(matrix_scaling * time(mountains[i-1], mountains[j-1]))

for j in range(1, np.shape(time_matrix)[0]): #coast to mountain j-1
    time_matrix[0][j] = int(matrix_scaling * time_coast(mountains[j-1], False))

for i in range(1, np.shape(time_matrix)[0]): #mountain i-1 to coast
    time_matrix[i][0] = int(matrix_scaling * time_coast(mountains[i-1], True))
np.set_printoptions(threshold=np.inf)
#print(time_matrix)
```
The data is stored in the dict `data` and is used by the solver along with the number of 'vehicles' (runners) and start/end point (0 refers to the row and column of `time_matrix` that represents the times to/from the coast).
```py
# --- Google OR-Tools TSP solver ---
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

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
```
The `distance_callback` feeds the solver the 'distances' (times) from `time_matrix` to use as the weights between nodes. The parameters of the solver are set as follows:
```py
transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC)
search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
search_parameters.time_limit.seconds = 60*5
#search_parameters.log_search = True
```
Multiple algorithms can be used. For example, the metaheuristic can be set to `SIMULATED_ANNEALING` but the current best results were with `GUIDED_LOCAL_SEARCH`. The `distance_callback` function is used to set the costs between nodes. Finally, the solution can be printed:
```py
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
            route_points.append(find_closest_coast(mountains[route[-2]-1].a, mountains[route[-2]-1].b))
        else:
            route_points.append((mountains[m-1].a, mountains[m-1].b))
    print('Route', i, route)
    print(len(route_points), ' route points: ', route_points)

# Final print formatting for q submission.
def print_final_solution(time=0.0, points=[]):
    print(round(time, 2))
    for point in points:
        print(str(point).strip('() '))
print_final_solution(solution.ObjectiveValue()/matrix_scaling, route_points) #confirm all solution printing is concordant
```
The function `get_routes` returns a list in the form `[0, 6, ... , 0]`. The route is then printed in coordinate form, which involves finding the coastal points for the mountains in position 1 and 60. This is printed as a list in the form `[(1, 28), (1, 27), ...]` which is easy to test (e.g. using the points to check the time is correct). However, the question demands the answer in a specific format. This is what `print_final_solution` provides.

The current best route, with a time of 93939.26s is shown below, plotted on [this Desmos graph](https://www.desmos.com/calculator/c4qiuqlpgy). The start point is (1, 28) and the end point is (15, 24). The circles show the bases of the mountains.

![best route](/final_q/finalq_jy/ritangle3_bestroute.png)