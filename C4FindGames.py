from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import msvcrt

# Correct path
PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"

# Create service object
service = Service(PATH)

# Start Chrome correctly
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

driver.get("https://papergames.io/en/match-history/6034f6c4e8d38d66cf92b549")

consent =  wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(@class, 'fc-cta-consent')]")
))
consent.click()

gameInfo = driver.find_element(By.ID, "serverApp-state")
raw_json = gameInfo.get_attribute("textContent")
data = json.loads(raw_json)

gamesInfo = data[list(data.keys())[1]]["b"]["rooms"]
for i in gamesInfo:
    print(i[list(i.keys())[1]])
    print(i[list(i.keys())[2]])
    print(i)
    break

while True:
    key = msvcrt.getch().decode().lower()
    if key == "x":
        break

#print("Browser open for 60 seconds...")
#time.sleep(600)

driver.quit()