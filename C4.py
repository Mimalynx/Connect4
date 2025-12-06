from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Correct path
PATH = r"C:\Users\Johan\Desktop\chromedriver-win64\chromedriver.exe"

# Create service object
service = Service(PATH)

# Start Chrome correctly
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

driver.get("https://papergames.io/en/connect4")
time.sleep(3)
search = driver.find_element(By.XPATH, "//button[contains(@class, 'fc-cta-consent')]")
search.click()

play_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[.//span[contains(text(), 'Play online')]]")
))
play_button.click()

nickname_input = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@placeholder='Nickname']")
))
nickname_input.clear()
nickname_input.send_keys("Mima")
nickname_input.send_keys(Keys.ENTER)
print("Nickname typed and confirmed!")

def my_label():
    board = [['.' for _ in range(7)] for _ in range(6)]
    for i in range(10000):
        try:
            for row in range(1, 7):       # 6 rows
                for col in range(1, 8):   # 7 columns
                    cell = driver.find_element(By.CSS_SELECTOR, f".cell-{row}-{col}")
                    circle = cell.find_element(By.TAG_NAME, "circle")

                    cls = circle.get_attribute("class")

                    if "empty-slot" in cls:
                        board[row-1][col-1] = '.'
                    elif "circle-light" in cls:
                        board[row-1][col-1] = 'L'   # Light color
                    elif "circle-dark" in cls:
                        board[row-1][col-1] = 'D'   # Dark color

            for row in range(1, 7):       # 6 rows
                row_str = ""
                for col in range(1, 8):   # 7 columns
                    row_str = row_str + " " + board[row-1][col-1]
                print(row_str)
            #time.sleep(0.1)
            print(i)
        except:
            try:
                leave_button = driver.find_element(By.XPATH, "//button[contains(text(),'Leave room')]")
                leave_button.click()
                time.sleep(3)
                play_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[contains(text(), 'Play online')]]")
                ))
                play_button.click()
                my_label() 
            except:
                time.sleep(3)


my_label()

print("Browser open for 60 seconds...")
time.sleep(60)



driver.quit()