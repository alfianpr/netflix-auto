#//////////////////////// PACKAGES /////////////////////////////

import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from sys import platform
from selenium.webdriver import ActionChains


#/////////////////// INFO & DEPENDENCIES //////////////////////

t1 = time.time()

#-------------------- Selenium Conf. --------------------------
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

# ser = Service('/users/kautsaraqsa/code/netflix-automation/v2/chromedriver_2')
# op = webdriver.ChromeOptions()
# op.add_experimental_option('excludeSwitches', ['enable-logging'])
# chromedriverpath = 'chromedriver'

#------------------------- URL --------------------------------
url_sp = 'https://www.netflix.com/changeplan'
url_cc = 'https://www.netflix.com/clearcookies'
url_yp = 'https://www.netflix.com/youraccount'

#---------------------- Credentials Testing ---------------------------

# email_id = 'lagasse@sneezers.space'   
# password = 'lebaran'
# email_list = [email_id]
# pass_list = [password]

#---------------------- Credentials Prod ---------------------------

data = np.loadtxt('down-plan.csv', delimiter= ',', skiprows= 1, dtype= str).T
email_list = data[0]
pass_list = data[1]
region = str(data[2][0])
n_acc = len(email_list)
 
#------------------------- Logs ------------------------------

log_file = open('downgrade_log.txt', 'a')

#/////////////////////// FUNCTION /////////////////////////////

def Click(element):
    driver.find_element(by = 'xpath', value = element).click()

def Filling(element, fill):
    field = driver.find_element(by = 'xpath', value = element)
    field.send_keys(fill)

def GetText(element):
    time.sleep(2)
    return driver.find_element(by = 'xpath', value = element).text

def ClearField(element):
    field = driver.find_element(by = 'xpath', value = element)
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)

def ScrollDown(value = 1) :
    page = driver.find_element(by = 'tag name', value = 'html')  
    for scroll in range(value):  
        page.send_keys(Keys.ARROW_DOWN) 

def logging(text):
    print(text)
    log_file.write(text)
    log_file.write('\n')
def ClearCookies():
    driver.get(url_cc)
    time.sleep(3)

#--------------------- Dictionary ---------------------------

plan_dict_brl = {
    'dasar_span': '//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/div[1]/label[1]/h2/span',
    'dasar': '//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/div[1]/label[1]/h2',
    'standar': '//*[@id="appMountPoint"]/div/div/div[2]/div/div/ul/li[2]',
    'premium': '//*[@id="appMountPoint"]/div/div/div[2]/div/div/div[2]/label[4]/h2',
    }

#--------------------- Change Plan --------------------------

def Upgrade(email_id, password):

    Output = '{} : Successful !'.format(email_id)

    global driver 

    driver.get(url_sp)   
    # time.sleep(2)

    try:
        Filling(element = '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div[1]/div/label/input', fill = email_id) #filling email
        Filling(element = '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input', fill = password) #filling password
    
    except:
        Filling(element = '/html/body/div[1]/div/div/div[2]/div/form/div[1]/div/div/input', fill = email_id) #filling email
        Filling(element = '/html/body/div[1]/div/div/div[2]/div/form/div[2]/div/div/input', fill = password) #filling password


    # time.sleep(1)
    
    try:
        Click(element= '/html/body/div[1]/div/div[3]/div/div/div[1]/form/button') #click 'sign in'
    
    except:
        Click(element= '//*[@id="appMountPoint"]/div/div/div[2]/div/form/button') #click 'sign in'
    
    time.sleep(2)

    try:
        Click(element= plan_dict_brl["dasar"])  #click plan
    
    except:
        Click(element= plan_dict_brl["dasar_span"])  #click plan 

    time.sleep(1)

    ScrollDown(value = 3)

    Click(element = '//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/div[2]/button[2]') #click 'Lanjut'

    time.sleep(1)

    try:
        Click(element = '//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/div[3]/div/footer/div/button[2]') #click 'confirm'

        time.sleep(1)
    except:
        current = GetText(element = '//*[@id="appMountPoint"]/div/div/div[2]/div/div/div/div[5]/div[1]/section/div[2]/div/div/div[1]/div[2]').split()[-1]
        Output = '{} : Current Plan -> {}'.format(email_id, current.upper())
        return Output

    time.sleep(1)
    driver.get(url_yp)

    try:
        next_bill_date = GetText(element='//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/div[5]/div[1]/section/div[2]/div/div/div[1]/div[1]/div/span')
    except:
        next_bill_date = GetText(element='//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/div[6]/div[1]/section/div[2]/div/div/div[1]/div[1]/div/span')
    
    balikdasar= GetText(element='//*[@id="automation-NextPlanItem"]')

    Output = '{} : {} : {}'.format(email_id, next_bill_date, balikdasar)

    ClearCookies()
    
    return Output

#///////////////////////// JOBS //////////////////////////////

#------------------------- RUN -----------------------------

logging('           Switch - Plan Job Logs            ')

logging('--------------------------------------------')

logging('///////////////// JOB START ////////////////')

for email, password in zip(email_list, pass_list):
    
    log_file = open('downgrade_log.txt', 'a')

    try:
        Output = Upgrade(email, password)
    except:    
        Output = '{} : DENIED'.format(email)

    logging(Output)

    # driver.close()

    log_file.close()

t2 = time.time()

print("Running Time = ", t2-t1)

driver.close()