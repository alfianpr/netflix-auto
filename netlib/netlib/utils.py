from selenium import webdriver
from sys import platform
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

import logging
from pathlib import Path

log_level = logging.DEBUG

# Print to the terminal
# resume = logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
#                     format="%(asctime)s %(levelname)s %(message)s")



def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)    

def driver_start():
    '''
    To open the browser. Using directory as input and action as output
    '''
    global driver, action
  
    op = webdriver.ChromeOptions()
    # prefs = {'download.default_directory': "directory"}
    # op.add_experimental_option('prefs', prefs)
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    op.add_argument('--ignore-ssl-errors=yes')
    op.add_argument('--ignore-certificate-errors')
    op.add_argument("--window-size=1920,1080")
    op.add_argument("--start-maximized")
    op.add_argument('--no-sandbox')
    op.add_argument("--disable-notifications")
    # op.add_argument("--headless=new")
    ser = Service(ChromeDriverManager().install())
    # if platform == "linux" or platform == "darwin":
    #     ser = Service(r'./chromedriver')
    # elif platform == "win32":
    #     ser = Service(r'./chromedriver.exe')
    driver = webdriver.Chrome(
        service = ser, 
        options = op
    )
    action = ActionChains(driver)
    return driver, action

def open_link(link):
    driver.get(link)

def click(element):
    driver.find_element(
        by = 'xpath',
        value = element
    ).click()

def filling(element, fill):
    driver.find_element(
        by = 'xpath', 
        value = element
    ).send_keys(fill)

def get_text(element):
    driver.find_element(
        by = 'xpath', 
        value = element
    ).text

def clear_field(element):
    field = driver.find_element(
        by = 'xpath', 
        value = element
    )
    field.send_keys([Keys.BACKSPACE] * 1000)

def scroll_down(value = 1) :
    page = driver.find_element(
        by = 'tag name',
        value = 'html'
    )  
    for i in range(value):  
        page.send_keys(Keys.ARROW_DOWN) 

def enter_key():
    action.send_keys(
        Keys.ENTER
    ).perform()

def close_driver():
    driver.close()

def screenshot(name):
    driver.get_screenshot_as_file(f"./screenshots/{name}.png")