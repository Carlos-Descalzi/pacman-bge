from levelmap import LEVEL_TEMPLATE
import random

MAZE_WIDTH=27
MAZE_HEIGHT=30
COMPLEXITY=0.75
DENSITY=0.75

def create_maze():
    shape = ((MAZE_HEIGHT // 2) * 2 + 1, (MAZE_WIDTH // 2) * 2 )
    complexity = int(COMPLEXITY * (5 * (shape[0] + shape[1])))
    density    = int(DENSITY * ((shape[0] // 2) * (shape[1] // 2)))
    maze = [list(l) for l in LEVEL_TEMPLATE]
    for i in range(density):
        while True:
            x, y = random.randint(0, shape[1] // 2) * 2, random.randint(0, shape[0] // 2) * 2
            if maze[y][x] in '# ':
                maze[y][x] = '#'
                break
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[random.randint(0, len(neighbours) - 1)]
                if maze[y_][x_] == ' ':
                    maze[y_][x_] = '#'
                    maze[y_ + (y - y_) // 2][x_ + (x - x_) // 2] = '#'
                    x, y = x_, y_

    pills = 4
    freeplaces = []
    for y,line in enumerate(maze):
        for x,row in enumerate(line):
            if row == ' ':
                freeplaces.append((y,x))

    pill_places = set(random.sample(freeplaces,4))
    start = set(random.sample(freeplaces,1))

    for y,line in enumerate(maze):
        for x in range(len(line)):
            pos = (y,x)
            if pos in pill_places:  line[x] = '*'
            elif pos in start:		line[x] = 'X'
            elif line[x] == ' ':    line[x] = '.'

    #print('\n'.join([''.join(l) for l in maze]))

    return maze

