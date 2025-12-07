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

listOfAllIds = ["6034f6c4e8d38d66cf92b549"]
listOfIds = ["6034f6c4e8d38d66cf92b549"]
listOfGames = []
start = True
bestPlayerId = "6034f6c4e8d38d66cf92b549"
bestPlayerElo = 0
#highElo = False
while(len(listOfIds) > 0):
    #print(bestPlayerId)
    #print(bestPlayerElo)
    print(len(listOfIds))
    print(len(listOfGames))
    idOfProfile = listOfIds.pop()
    driver.get("https://papergames.io/en/match-history/" + idOfProfile)

    if start == True:
        consent =  wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'fc-cta-consent')]")
        ))
        consent.click()
        start = False

    gameInfo = driver.find_element(By.ID, "serverApp-state")
    raw_json = gameInfo.get_attribute("textContent")
    data = json.loads(raw_json)
    gamesInfo = []
    try:
        if "rooms" in data[list(data.keys())[0]]["b"].keys():
            gamesInfo = data[list(data.keys())[0]]["b"]["rooms"]
        elif "rooms" in data[list(data.keys())[1]]["b"].keys():
            gamesInfo = data[list(data.keys())[1]]["b"]["rooms"]
        else:
            raise Exception("No room in data")
    except:
        continue

    minElo = 1700

    for i in gamesInfo:
        if i["gameType"] != "Connect4":
            continue
        if i["players"][0]["glicko2RatingRating"] < minElo:
            continue
        if i["players"][1]["glicko2RatingRating"] < minElo:
            continue
        print(i["uid"])
        if not (i["uid"] in listOfGames):
            listOfGames.append(i["uid"])

        if(not (i["players"][1]["accountId"] in listOfAllIds)):
            listOfIds.append(i["players"][1]["accountId"])
            listOfAllIds.append(i["players"][1]["accountId"])
            if i["players"][1]["glicko2RatingRating"] > bestPlayerElo:
                bestPlayerElo = i["players"][1]["glicko2RatingRating"] 
                bestPlayerId = i["players"][1]["accountId"]

        if(not (i["players"][0]["accountId"] in listOfAllIds)):
            listOfIds.append(i["players"][0]["accountId"])
            listOfAllIds.append(i["players"][0]["accountId"])
            if i["players"][0]["glicko2RatingRating"] > bestPlayerElo:
                bestPlayerElo = i["players"][0]["glicko2RatingRating"] 
                bestPlayerId = i["players"][0]["accountId"]
        #print(i.keys())
        #print(i)


while True:
    key = msvcrt.getch().decode().lower()
    if key == "x":
        break

#print("Browser open for 60 seconds...")
#time.sleep(600)

driver.quit()