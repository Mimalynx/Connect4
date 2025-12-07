from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import msvcrt

def select50():
    try:
        select_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "mat-select")
        ))
        driver.execute_script("arguments[0].click();", select_box)

        # click option 50
        option_50 = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//mat-option//span[contains(text(), '50')]")
        ))
        driver.execute_script("arguments[0].click();", option_50)
    except:
        print("error")
        select50()

PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"

service = Service(PATH)

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

listOfAllIds = ["6034f6c4e8d38d66cf92b549"]
listOfIds = ["6034f6c4e8d38d66cf92b549"]
start = True

while(len(listOfIds) > 0):

    print(len(listOfIds))
    print(len(listOfAllIds))

    idOfProfile = listOfIds.pop()
    driver.get("https://papergames.io/en/match-history/" + idOfProfile)
    time.sleep(0.5)
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

    for i in range(len(rows)):
        if elos[i] < minElo:
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
            print(candidateUser)
            print(elos[i])
        time.sleep(0.2)
    


while True:
    key = msvcrt.getch().decode().lower()
    if key == "x":
        break

#print("Browser open for 60 seconds...")
#time.sleep(600)

driver.quit()