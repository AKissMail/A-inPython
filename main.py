# This File is part of teh Assigment second Assigment of the NTNU curse TDT4136 in fall 2022.
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>
#
# Set up for the programm. It can solve all task from 1 to task To do so you need to set a task number in the variable
# task. The Path to the map has to be stored in the variable path_to_map.
# @param int task: between 1 and 4
# @param string path_to_map: the path to the map. The map should be present as a csv file.
# @author: Andreas Kißmehl - andrekis@stud.ntnu.no

# import of the A* implementation
from implementation_of_A_star import *

# config variables
task = 4
path_to_map = 'Samfundet_map_1.csv'  # there is a bug - see line 163 in implementation_of_A_star.py

if task == 1:
    start, goal = (18, 27), (32, 40)
elif task == 2:
    start, goal = (32, 40), (5, 8)
elif task == 3:
    start, goal = (32, 28), (32, 6)
elif task == 4:
    start, goal = (32, 6), (32, 28)
else:
    print('I dont know where to start :(')
    exit()

came_from, cost_so_far = a_star_search(create_diagram(47, 39, path_to_map), start, goal)
draw_grid(create_diagram(47, 39, ''), path=reconstruct_path(came_from, start=start, goal=goal))
print()
