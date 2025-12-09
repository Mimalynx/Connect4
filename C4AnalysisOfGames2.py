import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"
service = Service(PATH)

chrome_options = webdriver.ChromeOptions()
# Enable logging for performance/network
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(service=service, options=chrome_options)

# Enable network monitoring
driver.execute_cdp_cmd("Network.enable", {})

listOfCheckedGameIds = []

with open("ListOfAnalysisOfGames.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        listOfCheckedGameIds.append(parts[1])

with open("ListOfGames.txt") as file:
    listOfGames = [line.rstrip() for line in file]

while len(listOfGames) > 0:
    print(len(listOfGames))
    gameId = listOfGames.pop()
    if gameId in listOfCheckedGameIds:
        continue
    try:
        print(gameId)
        driver.get("https://papergames.io/en/r/" + gameId)
        time.sleep(5)
        moveString = ""
        breakBool = False

        myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f".cell-{1}-{1}")))
        count = 0
        while True:
            count += 1
            if count > 40:
                raise Exception("never exits")
            if breakBool:
                break
            logs = driver.get_log("performance")
            for entry in logs:
                msg = json.loads(entry["message"])["message"]
                if msg["method"] == "Network.responseReceived":
                    url = msg["params"]["response"]["url"]
                    if "xhr" in url or "socket.io" in url:
                        request_id = msg["params"]["requestId"]

                        body = driver.execute_cdp_cmd(
                            "Network.getResponseBody", {"requestId": request_id}
                        )
                        if body["body"][:3] == "431":
                            data = json.loads(body['body'][3:])
                            actions = data[1]["actions"]

                            for act in actions:
                                moveString = moveString + str(act["action"]["x"] + 1)
                            breakBool = True
                            break
        print(moveString)
        with open("ListOfAnalysisOfGames.txt", "a") as myfile:
            myfile.write(str(len(moveString)) + "," + gameId + "," + moveString + "\n")
    except Exception as error:
        print(error)
        continue

                