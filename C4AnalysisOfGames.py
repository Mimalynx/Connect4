from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import msvcrt

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
    firstWon = False
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
                    firstWon = True
                elif "circle-dark" in cls:
                    if board[row-1][col-1] == '.':
                        moveString = moveString + str(col)
                        gameStagnant = 0
                        #if not firstWon: raise Exception("Error: too fast placement 2")
                    board[row-1][col-1] = 'D'   # Dark color
                    firstWon = False
        #print(moveString)
        for row in range(1, 7):       # 6 rows
            row_str = ""
            for col in range(1, 8):   # 7 columns
                row_str = row_str + " " + board[row-1][col-1]
            #print(row_str)
    
    print(firstWon)
    print(gameId)
    print(moveString)