import pygame as pg
import time
import random

pg.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 4
NUM_ROWS = SCREEN_HEIGHT // CELL_SIZE
NUM_COLS = SCREEN_WIDTH // CELL_SIZE
SCREEN_WIDTH = CELL_SIZE * NUM_COLS
SCREEN_HEIGHT = CELL_SIZE * NUM_ROWS

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

color = None
color_gradient = [
    (255, 255, 255),  # White
    (0, 0, 255),  # Blue
    (42, 0, 213),
    (85, 0, 170),
    (128, 0, 128),  # Purple
    (85, 0, 85),
    (42, 0, 42),
    (0, 0, 0),  # Black
]

grid = [
    [[7, 0, 0] for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)
]  # grid[i][j] = [colorIndex, neighbor count, lastUpdated]

decaying = set()  # [i, j]
whiteCells = set()  # [i, j]


def handlePreGame():
    global drawing
    global preGame
    global game
    global grid
    global whiteCells

    for event in pg.event.get():
        if event.type == pg.QUIT:
            preGame = False
            break
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                x, y = event.pos
                x = x // CELL_SIZE
                y = y // CELL_SIZE
                if 0 <= y < NUM_ROWS and 0 <= x < NUM_COLS:
                    grid[y][x] = [0, 0, 0]
                    pg.draw.rect(
                        screen,
                        color_gradient[0],
                        (
                            x * CELL_SIZE,
                            y * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        ),
                    )
                    print(y, x, NUM_ROWS, NUM_COLS)
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
        elif event.type == pg.MOUSEMOTION and drawing:
            x, y = event.pos
            x = x // CELL_SIZE
            y = y // CELL_SIZE
            # print("here MOVING", x, y)
            if 0 <= y < NUM_ROWS and 0 <= x < NUM_COLS:
                grid[y][x] = [0, 0, 0]
                pg.draw.rect(
                    screen,
                    color_gradient[0],
                    (
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            game = True
            preGame = False
            for i in range(NUM_ROWS):
                for j in range(NUM_COLS):
                    if grid[i][j][0] == 0:
                        whiteCells.add((i, j))


def handleGame():
    global gameTime
    global game
    global whiteCells
    global decaying

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
            return

    gameTime += 1
    toRemove = []
    for y, x in decaying:
        if grid[y][x][0] == 7:
            toRemove.append([y, x])
        else:
            grid[y][x][0] += 1
            grid[y][x][1] = 0
            grid[y][x][2] = gameTime
            pg.draw.rect(
                screen,
                color_gradient[grid[y][x][0]],
                (
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )
    for Y, X in toRemove:
        decaying.remove((Y, X))
    toRemove.clear()

    for i, j in whiteCells:
        decaying.add((i, j))
        grid[i][j][2] = gameTime
        grid[i][j][1] = 0
        if grid[i][j][0] != 0:
            grid[i][j][0] = 0
        pg.draw.rect(
            screen,
            color_gradient[0],
            (
                j * CELL_SIZE,
                i * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )
    newWhiteCells = set()

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    def isIn(i, j):
        if 0 <= i < NUM_ROWS and 0 <= j < NUM_COLS:
            return True
        return False

    for I, J in whiteCells:
        for d1, d2 in dirs:
            if isIn(I + d1, J + d2):
                nI, nJ = I + d1, J + d2
                if grid[nI][nJ][2] < gameTime:
                    grid[nI][nJ][1] = 1
                    grid[nI][nJ][2] = gameTime
                else:
                    grid[nI][nJ][1] += 1
                count = grid[nI][nJ][1]
                if grid[nI][nJ][0] == 0:
                    if count == 2 or count == 3:
                        newWhiteCells.add((nI, nJ))
                    elif count == 4:
                        newWhiteCells.remove((nI, nJ))
                else:
                    if count == 3:
                        newWhiteCells.add((nI, nJ))
                    elif count == 4:
                        newWhiteCells.remove((nI, nJ))
    whiteCells = newWhiteCells


gameTime = 0
drawing = False
preGame = True
game = False

while preGame or game:
    if preGame:
        handlePreGame()
    elif game:
        handleGame()
    # print(gameTime)
    pg.display.update()
    if game:
        time.sleep(0.01)
pg.quit()
