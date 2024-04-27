import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from sys import platform
from selenium.webdriver import ActionChains

op = webdriver.ChromeOptions()
# prefs = {'download.default_directory': "directory"}
# op.add_experimental_option('prefs', prefs)
op.add_experimental_option('excludeSwitches', ['enable-logging'])
op.add_argument('--ignore-ssl-errors=yes')
op.add_argument('--ignore-certificate-errors')
# op.add_argument("--window-size=1920,1080")
# op.add_argument("--start-maximized")
op.add_argument('--no-sandbox')
op.add_argument("--disable-notifications")
# op.add_argument("--headless=new")
# ser = Service(ChromeDriverManager().install())
if platform == "linux" or platform == "darwin":
    ser = Service(r'./webdriver/chromedriver')
elif platform == "win32":
    ser = Service(r'./webdriver/chromedriver.exe')
driver = webdriver.Chrome(
    service = ser, 
    options = op
)
action = ActionChains(driver)

