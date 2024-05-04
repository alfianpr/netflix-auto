from netlib.cplib import *
import json
import time
import pandas as pd

t1 = time.time()
log_file = open('downgrade_log.txt', 'a')

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTQ2w3lo__BTgmboUSYSDjVgy5dopC-2vgHbvojbUNbxXe8I0qbCHGeGSzsJOeugSGO-1wm-rv3mlsd/pub?gid=0&single=true&output=csv')

def Upgrade(email_id, password):
    Output = '{} : Successful !'.format(email_id)
    open_link(
        link=json.load(
            open("config/cp_url.json"))["url_sp"]
    )
    time.sleep(2)
    try:
        Filling(
            element=json.load(open("config/cp_element.json"))["filling_email_1"], 
            fill = email_id
        ) #filling email
        Filling(
            element=json.load(open("config/cp_element.json"))["filling_password_1"],
            fill = password
        ) #filling password
    
    except:
        Filling(
            element=json.load(open("config/cp_element.json"))["filling_email_2"],
            fill = email_id
        ) #filling email
        Filling(
            element=json.load(open("config/cp_element.json"))["filling_password_2"],
            fill = password
        ) #filling password
    try:
        Click(
            element=json.load(open("config/cp_element.json"))["sign_in_1"],
        ) #click 'sign in'
    except:
        Click(
            element=json.load(open("config/cp_element.json"))["sign_in_2"],
        ) #click 'sign in'
    time.sleep(2)
    try:
        Click(
            element=json.load(open("config/cp_element.json"))["dasar"]
        )  #click plan
    
    except:
        Click(
            element=json.load(open("config/cp_element.json"))["dasar_span"]
        )  #click plan 
    time.sleep(1)
    ScrollDown(value = 3)
    # Click Lanjut
    Click(
        element=json.load(open("config/cp_element.json"))["click_lanjut"]
    )
    time.sleep(1)
    try:
        Click(
            element=json.load(open("config/cp_element.json"))["click_confirm"]
        ) #click 'confirm'
        time.sleep(1)
    except:
        current = GetText(
            element=json.load(open("config/cp_element.json"))["current_plan"]
        ).split()[-1]
        Output = '{} : Current Plan -> {}'.format(email_id, current.upper())
        return Output
    time.sleep(1)
    open_link(
        link=json.load(open("config/cp_url.json"))["url_yp"]
    )
    try:
        next_bill_date = GetText(
            element=json.load(open("config/cp_element.json"))["next_bill_date_1"]
        )
    except:
        next_bill_date = GetText(
            element=json.load(open("config/cp_element.json"))["next_bill_date_2"]
        )
    balikdasar= GetText(
        element=json.load(open("config/cp_element.json"))["balik_dasar"]
    )
    Output = '{} : {} : {}'.format(email_id, next_bill_date, balikdasar)
    # CLear cookies
    open_link(
        link=json.load(open("config/cp_url.json"))["url_cc"]
    )
    time.sleep(3)

    return Output

def flow():
    driver_start()
    dict = df.to_dict("records")
    log_file = open('downgrade_log.txt', 'a')
    logging('           Switch - Plan Job Logs            ')

    logging('--------------------------------------------')

    logging('///////////////// JOB START ////////////////')
    for i in dict:
        email = i["email"]
        password = i["password"]

        log_file = open('downgrade_log.txt', 'a')

        try:
            Output = Upgrade(email, password)
        except:    
            Output = '{} : DENIED'.format(email)

        Upgrade(
            email_id=email,
            password=password
        )
        logging(Output)
        log_file.close()

    t2 = time.time()

    print("Running Time = ", t2-t1)
    close_driver()

if __name__ == "__main__":
    flow()