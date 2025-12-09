import pygame
import sys
import numpy as np


class Node:
    def __init__(self):
        self.children = {}
        self.count = 0
        self.playerOnesTurn = True
        self.winCount = 0

root = Node()

movesInGames = []
whoWon = []
with open("ListOfAnalysisOfGames.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        movesInGames.append(parts[2])
        whoWon.append(int(parts[0]) % 2 != 0)

for i in range(len(movesInGames)):
    current = root
    current.count += 1
    current.playerOnesTurn = True
    if whoWon[i]:
        current.winCount += 1

    for move in movesInGames[i]:
        if move not in current.children:
            current.children[move] = Node()

        current.children[move].playerOnesTurn = not current.playerOnesTurn
        current = current.children[move]
        if whoWon[i] != current.playerOnesTurn:
            current.winCount += 1
        current.count += 1

# Constants
ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4")
font = pygame.font.SysFont("monospace", 50)

board = np.zeros((ROWS, COLS))
turn = 0

def get_next_open_row(board, col):
    for r in range(ROWS-1,-1,-1):
        if board[r][col] == 0:
            return r


def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(
                screen, (0, 0, 255),
                (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )
            color = (0, 0, 0)
            if board[r][c] == 1:
                color = (255, 0, 0)
            elif board[r][c] == 2:
                color = (255, 255, 0)

            pygame.draw.circle(
                screen, color,
                (int(c * SQUARESIZE + SQUARESIZE / 2),
                 int(r * SQUARESIZE + SQUARESIZE / 2)),
                RADIUS
            )
    pygame.display.update()

def reset_board():
    global board, turn, gameState
    board[:] = 0
    turn = 0
    gameState = root
    print("RESET")

def draw_text(text, x, y, size=32, color=(255,255,255)):
    font = pygame.font.SysFont("monospace", size, bold=True)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

draw_board(board)

gameState = root
for i in range(1,8):
    print(str(gameState.children[str(i)].winCount) + "/" + str(gameState.children[str(i)].count))
    #print(root.children["4"].children["3"].children[str(i)].winCount)
    gameState.children["4"].children[str(i)].count



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_board()
                draw_board(board)

                gameState = root
                for i in range(1,8):
                    print(str(gameState.children[str(i)].winCount) + "/" + str(gameState.children[str(i)].count))

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = posx // SQUARESIZE

            gameState = gameState.children[str(col + 1)]

            pygame.draw.rect(
                screen, (0, 0, 0),
                (0, 6 * SQUARESIZE, 7*SQUARESIZE, SQUARESIZE)
            )
            
            for i in range(1,8):
                if str(i) not in gameState.children:
                    gameState.children[str(i)] = Node()
                print(str(gameState.children[str(i)].winCount) + "/" + str(gameState.children[str(i)].count))
                draw_text(str(gameState.children[str(i)].winCount), (i-1)*SQUARESIZE, 6*SQUARESIZE, size=32, color=(255,255,255))
                draw_text("/"+str(gameState.children[str(i)].count), (i-1)*SQUARESIZE, 6.5*SQUARESIZE, size=32, color=(255,255,255))
            if board[0][col] == 0:
                row = get_next_open_row(board, col)
                board[row][col] = turn + 1

                turn = 1 - turn

            draw_board(board)