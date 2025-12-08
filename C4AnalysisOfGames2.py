import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"
service = Service(PATH)

chrome_options = webdriver.ChromeOptions()
# Enable logging for performance/network
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(service=service, options=chrome_options)

# Enable network monitoring
driver.execute_cdp_cmd("Network.enable", {})
#driver.get("https://papergames.io/en/r/wPSJuKRfLy")
driver.get("https://papergames.io/en/r/OrVDGSqG3q")
moveString = ""
breakBool = False

while True:
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

                