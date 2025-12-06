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


# Correct path
PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"

# Create service object
service = Service(PATH)

# Start Chrome correctly
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

listOfAllIds = ["6034f6c4e8d38d66cf92b549"]
listOfIds = ["6034f6c4e8d38d66cf92b549"]
listOfGames = []
start = True

idOfProfile = listOfIds.pop()
driver.get("https://papergames.io/en/match-history/" + idOfProfile)

if start == True:
    consent =  wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'fc-cta-consent')]")
    ))
    consent.click()
    start = False


j = 0
while True:
    select50()

    time.sleep(1)  # give table time to load
    print("test2")

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.mat-mdc-row")
    match_ids = []

    readyChangePage = True
    for i in range(len(rows)):
        print(i)
        select50()

        if readyChangePage:
            for k in range(j):
                print("test")
                next_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.mat-mdc-paginator-navigation-next")
                ))
                driver.execute_script("arguments[0].click();", next_button)
            readyChangePage = False
        
        time.sleep(0.2)
        try:
            row = driver.find_elements(By.CSS_SELECTOR, "tr.mat-mdc-row")[i]
            #match_id = driver.execute_script("return arguments[0].__ngContext__", row)
            #print(match_id)
            #print(row.get_attribute("outerHTML"))
            #print(driver.find_elements(By.CSS_SELECTOR, "tr.mat-mdc-row"))
            row.click()
            time.sleep(0.2)  # wait for page navigation
            url = driver.current_url
            print(url)
            match_ids.append(url)
            driver.back()
            time.sleep(0.2)  # wait to return
            readyChangePage = True
        except:
            print("test3")
            continue

    j += 1
    print(match_ids)



while True:
    key = msvcrt.getch().decode().lower()
    if key == "x":
        break

#print("Browser open for 60 seconds...")
#time.sleep(600)

driver.quit()