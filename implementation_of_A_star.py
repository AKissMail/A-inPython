# The base for the implementation was the A* implementation from redblobgames.com.
# It can be found under https://www.redblobgames.com/pathfinding/a-star/ - Copyright 2014 Red Blob Games
# Contact to redblobgames : redblobgames@gmail.com
#
# Modifications done by Andreas Kißmehl for the second Assigment of the NTNU curse TDT4136 in fall 2022.
# First of all I remove a lot of things from the File. The next modification is the Function read_samfundet_data and
# create_diagram wich will take a given path, load an csv file and create out of that file a graph object.
# @author: redblobgames - redblobgames@gmail.com
# @author: Andreas Kißmehl - andrekis@stud.ntnu.no
# @License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

# imports
from __future__ import annotations
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
import csv
import heapq

# Variables
GridLocation = Tuple[int, int]
Location = TypeVar('Location')
T = TypeVar('T')


# classes

# This class represents the Graph.
class Graph(Protocol):
    def neighbors(self, id: Location) -> list[Location]: pass


# This class represents the Graph with weights.
class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass


# Implementations of a priorityQueue for the A* implementation.
class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


# This class implements the grid with the weights.
class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)


# utility functions for dealing with square grids
def from_id_width(id, width):
    return id % width, id // width


# This function create the individual characters for the map.
# @param graph: the graph of the map
# @param id: determine wich carter should be used
# @param style: the style to be used for the output
# @return: the characters of the line

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']:
        r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1:
            r = " > "
        if x2 == x1 - 1:
            r = " < "
        if y2 == y1 + 1:
            r = " v "
        if y2 == y1 - 1:
            r = " ^ "
    if 'path' in style and id in style['path']:
        r = " @ "
    if 'start' in style and id == style['start']:
        r = " A "
    if 'goal' in style and id == style['goal']:
        r = " Z "
    if id in graph.walls:
        r = "###"
    return r


# This function create a console representation ot the map and the path.
# @param graph: the graph that be created
# @param **style: the style to be used for the output
def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)


# This function is used to creat an array out of a given csv file.
# The file will be searched for a given token.
# If this token was fond, the function will return an array of tokens with their positions.
# @param filename: The path to the csv file containing the map
# @param token: The token to search in the csv file.
def read_samfundet_data(filename, token):
    int_row = 0
    results = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            int_item = 0
            for item in row:
                if item == token:
                    results.append((int_item, int_row))
                int_item = int_item + 1
            int_row = int_row + 1
    return results


# This is a helper function with create a Graph that A* can use.
# This Graph has an x and y size and a some data.
# This data has to be provided as csv data.
# Each cell is a point a can have a wight between 0 and 4.
# @param int height: that is the height of the map.
# @param int width: that is the width of the map.
# @param map_data: that is the path to the map data.
# @return: the graph according to the map data.
def create_diagram(height, width, map_data):
    # I was not abel to get to work. For some reason the path as string get lost.
    # If I just try example.csv in main.py, I got hier an empty sting ''.
    # If I try example that works, but if when add in 168 the .csv, I just got '.csv'
    # Me, the Internet and tow TA where not able to find the reason, so I just bypass it in 171.
    # Not nice, but it work.
    # print('print map_data:' + map_data)  # todo
    # file_end = '.csv'
    # map_data = map_data + file_end
    map_data = 'Samfundet_map_Edgar_full.csv'
    map_diagram = GridWithWeights(width, height)
    map_diagram.walls = read_samfundet_data(map_data, '-1')
    map_diagram.weights = {loc: 1 for loc in read_samfundet_data(map_data, '1')}
    map_diagram.weights = {loc: 2 for loc in read_samfundet_data(map_data, '2')}
    map_diagram.weights = {loc: 3 for loc in read_samfundet_data(map_data, '3')}
    map_diagram.weights = {loc: 4 for loc in read_samfundet_data(map_data, '4')}

    return map_diagram


# This Function reconstruct the path wich will provide an answer if a path was found or not.
# @param came_from: the result of the a_star_search algorithm
# @return path: In the case that the path was not found it will return an empty array.
#               In the case that the path was found it will return the path in an array.
#               The format should look like this: [(x,y),...,(x,y)]
def reconstruct_path(came_from: dict[Location, Location],
                     start: Location, goal: Location) -> list[Location]:
    current: Location = goal
    path: list[Location] = []
    if goal not in came_from:  # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    return path


# a Variable that uses a Function from GridWithWeights.
# That why it has to be hier and not with his buddy's at the top.
diagram_nopath = GridWithWeights(10, 10)
diagram_nopath.walls = [(5, row) for row in range(10)]


# This is the heuristic function wich is used by A*
# Is uses the manhattan distance to estimate the distance between the tow given points.
# @param a: Expect a GridLocation with tow points
# @param b: Expect a GridLocation with tow points
# @return: the estimate of the distance between a and b.
def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


# This function is the A* Search Algorithm.
# As input, it takes a graph object, a start and end point.
# In any case is will call the function reconstruct_path.
# reconstruct_path will evaluate if a path was found or not.
# @param graph: an instance of the class graph
# @param start: the start point
# @param goal: the end point
# @return came_from: a list of nodes with describe the path
# @return cost_so_far: the cost of the found path
def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far
