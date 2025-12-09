from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import msvcrt
import random

def select50():
    select_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "mat-select")
    ))
    driver.execute_script("arguments[0].click();", select_box) 

    option_50 = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-option//span[contains(text(), '50')]")
    ))
    driver.execute_script("arguments[0].click();", option_50)

PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"

service = Service(PATH)

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 5)

#listOfAllIds = ["6034f6c4e8d38d66cf92b549"]
#listOfIds = ["6034f6c4e8d38d66cf92b549"]
#NameList = ["angel 77"]

#with open("ListOfPlayers.txt") as file:
#    listOfAllIds = [line.rstrip() for line in file]
    
#with open("ListOfPlayers.txt") as file:
#    listOfIds = [line.rstrip() for line in file]
#NameList = []

listOfAllIds = []
listOfIds = []
NameList = []

with open("ListOfPlayers.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        listOfAllIds.append(parts[1])
        listOfIds.append(parts[1])
        NameList.append(parts[0])

start = True

while(len(listOfIds) > 0):
    try:
        print(len(listOfIds))
        print(len(listOfAllIds))

        idOfProfile = listOfIds.pop(random.randint(0,len(listOfIds)-1))
        print(idOfProfile)
        driver.get("https://papergames.io/en/match-history/" + idOfProfile)
        time.sleep(0.5)
        #wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        if start == True:
            consent =  wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'fc-cta-consent')]")
            ))
            consent.click()
            start = False

        minElo = 1850
        select50()
        time.sleep(0.5)
        rows = driver.find_elements(By.CSS_SELECTOR, "div.user-profile.cursor-pointer")
        eloList = driver.find_elements(By.CLASS_NAME, "c-gray-700")[1:]
        elos = [int(el.text[1:-1]) for el in eloList]

        name_elements = driver.find_elements(By.CLASS_NAME, "user-profile")
        names = [el.text for el in name_elements]

        gamesData = driver.find_elements(By.CSS_SELECTOR, "td.cdk-column-gameType")
        games = [el.text.strip() for el in gamesData]

        for i in range(len(rows)):
            try:
                if elos[i] < minElo:
                    continue
                if names[i] in NameList:
                    continue
                if games[int(i/2)] != "Connect 4":
                    print(games[int(i/2)])
                    continue
                row = rows[i]
                #row.click()
                driver.execute_script("arguments[0].click();", row)
                time.sleep(0.2)
                button = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        "button.mat-mdc-menu-trigger"
                    ))
                )
                driver.execute_script("arguments[0].click();", button)
                history_item = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//a[@mat-menu-item]//span[text()='History']/parent::a"
                    ))
                )
                href = history_item.get_attribute("href")
                candidateUser = href[39:]
                if(not(candidateUser in listOfAllIds)):
                    listOfAllIds.append(candidateUser)
                    listOfIds.append(candidateUser)
                    NameList.append(names[i])
                    print(candidateUser)
                    print(elos[i])
                    try:
                        with open("ListOfPlayers.txt", "a") as myfile:
                            myfile.write(names[i] + "," + candidateUser + "," + str(elos[i]) + "\n")
                    except Exception as e:
                        print("File write error:", e)
                else:
                    NameList.append(names[i])
                time.sleep(0.2)
            except:
                print("error 1")
                continue
    except Exception as error:
        print("error 2")
        print(error)
        continue
    


while True:
    key = msvcrt.getch().decode().lower()
    if key == "x":
        break

#print("Browser open for 60 seconds...")
#time.sleep(600)

driver.quit()