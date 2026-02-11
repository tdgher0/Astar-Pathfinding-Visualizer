import pygame
from queue import PriorityQueue

pygame.init()

WIDTH = 600
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Simple A* Demo")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREY = (200, 200, 200)

grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]
start = None
end = None

def draw():
    WIN.fill(WHITE)
    gap = WIDTH // ROWS
    for i in range(ROWS):
        for j in range(ROWS):
            color = WHITE
            if grid[i][j] == 1: color = BLACK
            if grid[i][j] == 2: color = ORANGE
            if grid[i][j] == 3: color = BLUE
            if grid[i][j] == 4: color = GREEN
            if grid[i][j] == 5: color = RED
            if grid[i][j] == 6: color = PURPLE
            pygame.draw.rect(WIN, color, (j*gap, i*gap, gap, gap))
            pygame.draw.rect(WIN, GREY, (j*gap, i*gap, gap, gap), 1)
    pygame.display.update()

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    if x > 0: neighbors.append((x-1, y))
    if x < ROWS-1: neighbors.append((x+1, y))
    if y > 0: neighbors.append((x, y-1))
    if y < ROWS-1: neighbors.append((x, y+1))
    return neighbors

def astar():
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g = { (i,j): float("inf") for i in range(ROWS) for j in range(ROWS) }
    g[start] = 0

    while not open_set.empty():
        current = open_set.get()[1]

        if current == end:
            while current in came_from:
                current = came_from[current]
                if current != start:
                    grid[current[0]][current[1]] = 6
                draw()
            return

        for neighbor in get_neighbors(current):
            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            temp_g = g[current] + 1
            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f = temp_g + heuristic(neighbor, end)
                open_set.put((f, neighbor))
                if neighbor != end:
                    grid[neighbor[0]][neighbor[1]] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw()

def get_clicked_pos(pos):
    gap = WIDTH // ROWS
    x, y = pos
    return y // gap, x // gap

running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            row, col = get_clicked_pos(pygame.mouse.get_pos())
            if not start:
                start = (row, col)
                grid[row][col] = 2
            elif not end:
                end = (row, col)
                grid[row][col] = 3
            else:
                grid[row][col] = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                astar()
            if event.key == pygame.K_c:
                grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]
                start = None
                end = None

pygame.quit()
