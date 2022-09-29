# import Map
from implementation import *

# Set up for the redblobgames version of the Algorithm
task = 4
if task == 1:
    start, goal = (18, 27), (32, 40)
    path_to_map = 'Samfundet_map_1'
elif task == 2:
    start, goal = (32, 40), (5, 8)
    path_to_map = 'Samfundet_map_1'
elif task == 3:
    start, goal = (32, 28), (32, 6)
    path_to_map = 'Samfundet_map_2'
elif task == 4:
    start, goal = (32, 6), (32, 28)
    path_to_map = 'Samfundet_map_Edgar_full'
else:
    print('I dont know where to start')
    exit()

came_from, cost_so_far = a_star_search(create_diagram(47, 39, path_to_map), start, goal)
draw_grid(create_diagram(47, 39, ''), path=reconstruct_path(came_from, start=start, goal=goal))
print()

# Map.Map_Obj.show_map(draw_grid(diagram4, path=reconstruct_path(came_from, start=start, goal=goal)))
