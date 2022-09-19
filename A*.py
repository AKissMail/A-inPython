import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("my wonderful implementation of A*")

# todo define colors
WHITE = (255, 255, 255)
CLOSED = (0, 0, 0)
OPEN = (0, 0, 0)
BARRIER = (0, 0, 0)
START = (0, 255, 0)
END = (255, 0, 0)
PATH = (0, 0, 0)
LINE = (0, 0, 0)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.colors = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.colors == CLOSED

    def is_open(self):
        return self.colors == OPEN

    def is_barrier(self):
        return self.colors == BARRIER

    def is_start(self):
        return self.colors == START

    def is_end(self):
        return self.colors == END

    def reset(self):
        self.colors = WHITE

    def make_closed(self):
        return self.colors == CLOSED

    def make_open(self):
        self.colors = OPEN

    def make_barrier(self):
        self.colors = BARRIER

    def make_start(self):
        self.colors = START

    def make_end(self):
        self.colors = END

    def make_path(self):
        self.colors = PATH

    def draw(self, win):
        pygame.draw.rect(win, self.colors, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def algorith(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    #todo https://youtu.be/JtiK0DOeI4A?t=4521


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, LINE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, LINE, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # LEFT
                row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    node.make_start()

                elif not end and node != start:
                    end = node
                    node.make_end()

                elif node != end and node != start:
                    node.make_barrier()



            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors()
                    algorith(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()


main(WIN, WIDTH)
