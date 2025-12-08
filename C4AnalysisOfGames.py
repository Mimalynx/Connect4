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


with open("ListOfGames.txt") as file:
    listOfGames = [line.rstrip() for line in file]

while(len(listOfGames) > 0):
    #gameId = "GERXuah0uV"
    gameId = listOfGames.pop()
    print(len(listOfGames))

    driver.get("https://papergames.io/en/r/" + gameId)

    time.sleep(2)

    board = [['.' for _ in range(7)] for _ in range(6)]
    whoWon = ""
    moveString = ""
    gameStagnant = 0

    while(gameStagnant < 3):
        gameStagnant += 1
        for row in range(1, 7):       # 6 rows
            for col in range(1, 8):   # 7 columns
                cell = driver.find_element(By.CSS_SELECTOR, f".cell-{row}-{col}")
                circle = cell.find_element(By.TAG_NAME, "circle")

                cls = circle.get_attribute("class")

                if "empty-slot" in cls:
                    board[row-1][col-1] = '.'
                elif "circle-light" in cls:
                    if board[row-1][col-1] == '.':
                        moveString = moveString + str(col)
                        gameStagnant = 0
                        #if firstWon: raise Exception("Error: too fast placement 1")
                    board[row-1][col-1] = 'L'   # Light color
                    if won(board) == 'L':
                        gameStagnant = 10000
                        whoWon = "L"
                elif "circle-dark" in cls:
                    if board[row-1][col-1] == '.':
                        moveString = moveString + str(col)
                        gameStagnant = 0
                        #if not firstWon: raise Exception("Error: too fast placement 2")
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
    
    if whoWon != "":
        with open("ListOfAnalysisOfGames.txt", "a") as myfile:
            myfile.write(whoWon + "," + gameId + "," + moveString + "\n")
        print(whoWon)
        print(gameId)
        print(moveString)