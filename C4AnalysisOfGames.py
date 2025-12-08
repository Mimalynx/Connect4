from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import msvcrt

def won(board):
    #horizontal
    for row in range(0, 6):     
        for col in range(0, 4):
            if(board[row][col] != "." and board[row][col] == board[row][col + 1] and board[row][col] == board[row][col + 2] and board[row][col] == board[row][col + 3]):
                return board[row][col]
    #vertical
    for row in range(0, 3):     
        for col in range(0, 7):
            if(board[row][col] != "." and board[row][col] == board[row + 1][col] and board[row][col] == board[row + 2][col] and board[row][col] == board[row + 3][col]):
                return board[row][col]
    #diag1
    for row in range(0, 3):     
        for col in range(0, 4):
            if(board[row][col] != "." and board[row][col] == board[row + 1][col + 1] and board[row][col] == board[row + 2][col + 2] and board[row][col] == board[row + 3][col + 3]):
                return board[row][col]
    #diag2
    for row in range(0, 3):     
        for col in range(3, 7):
            if(board[row][col] != "." and board[row][col] == board[row + 1][col - 1] and board[row][col] == board[row + 2][col - 2] and board[row][col] == board[row + 3][col - 3]):
                return board[row][col]
            

PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"

service = Service(PATH)

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

with open("ListOfGamesIdNotEnded.txt", "r") as f:
    testedIds = [line.rstrip() for line in f]

with open("ListOfAnalysisOfGames.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        testedIds.append(parts[1])
        #print(parts[1])

with open("ListOfGames.txt") as file:
    listOfGames = [line.rstrip() for line in file]

while(len(listOfGames) > 0):
    #gameId = "GERXuah0uV"
    gameId = listOfGames.pop()
    print(gameId)
    if gameId in testedIds:
        continue
    print(len(listOfGames))

    board = [['.' for _ in range(7)] for _ in range(6)]
    whoWon = ""
    moveString = ""
    gameStagnant = 0
    turn = 0
    turnPlayer = ""
    driver.get("https://papergames.io/en/r/" + gameId)
    height = [6,6,6,6,6,6,6]

    time.sleep(0.5)
    try:
        WaitForLoad = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f".cell-{1}-{1}")
        ))
    except Exception as error:
        print(error)
        continue

    try:
        while(gameStagnant < 6):
            time.sleep(0.5)
            gameStagnant += 1
            for row in range(1, 7):       # 6 rows
                for col in range(1, 8):   # 7 columns
                    if height[col-1] != row:
                        #print("test")
                        #print(height[col-1])
                        #print(row)
                        continue
                    cell = driver.find_element(By.CSS_SELECTOR, f".cell-{row}-{col}")
                    circle = cell.find_element(By.TAG_NAME, "circle")

                    cls = circle.get_attribute("class")

                    if "empty-slot" in cls:
                        board[row-1][col-1] = '.'
                    elif "circle-light" in cls:
                        height[col-1] -= 1
                        if board[row-1][col-1] == '.':
                            moveString = moveString + str(col)
                            gameStagnant = 0
                            #if turn % 2 != 1: raise Exception("moves out of order1")
                            if turnPlayer == "D": raise Exception("moves out of order1")
                            turnPlayer = "D"
                            turn = turn + 1
                        board[row-1][col-1] = 'L'   # Light color
                        if won(board) == 'L':
                            gameStagnant = 10000
                            whoWon = "L"
                    elif "circle-dark" in cls:
                        height[col-1] -= 1
                        if board[row-1][col-1] == '.':
                            moveString = moveString + str(col)
                            gameStagnant = 0
                            #if turn % 2 != 0: raise Exception("moves out of order2")
                            if turnPlayer == "L": raise Exception("moves out of order1")
                            turnPlayer = "L"
                            turn = turn + 1
                        board[row-1][col-1] = 'D'   # Dark color
                        if won(board) == 'D':
                            gameStagnant = 10000
                            whoWon = "D"
            #print(moveString)
            #for row in range(1, 7):       # 6 rows
            #    row_str = ""
            #    for col in range(1, 8):   # 7 columns
            #        row_str = row_str + " " + board[row-1][col-1]
            #    print(row_str)
    except Exception as error:
        print(error)
        continue

    if whoWon != "":
        with open("ListOfAnalysisOfGames.txt", "a") as myfile:
            myfile.write(str(turn) + "," + gameId + "," + moveString + "\n")
        print(turn)
        print(gameId)
        print(moveString)
    else:
        with open("ListOfGamesIdNotEnded.txt", "a") as myfile:
            myfile.write(gameId + "\n")