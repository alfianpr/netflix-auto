from netlib.utils import (
    open_link,
    driver_start,
    log,
    filling,
    enter_key,
    click,
    clear_field,
    close_driver,
    get_text,
    screenshot
)
import json
import argparse
import pandas as pd
import time
from datetime import datetime

# Setup the input
parser = argparse.ArgumentParser(description="Input the number of hackback credentials")
parser.add_argument("-n", help="input the number")
args = parser.parse_args()
CREDENTIAL = f"hackback_login_{args.n}"

# Load the requirements files
PAGE_URL = json.load(open("config/hackback_url.json"))
PAGE_ELEMENT = json.load(open("config/hackback_element.json"))
CREDENTIAL_DF = pd.read_csv(f"credential/{CREDENTIAL}.csv")
NEW_PASS_LISTS = json.load(open(f"credential/hackback_newpass.json"))

# Login to the netflix
def login(email_id, password):
    # try:
    open_link(PAGE_URL["url_tp"])
    log.info(f"Login to netflix {PAGE_URL['url_tp']}")
    time.sleep(3)
    filling(PAGE_ELEMENT["email_login"], email_id)
    log.info(f"Input email {email_id}")
    filling(PAGE_ELEMENT["password_login"], password)
    log.info(f"Input password {password}")
    enter_key()

# Turn off the TP
def tp_off(email_id):
    try:
        log.info(f"Turn on the TP for {email_id}")
        try:
            time.sleep(1)
            click(PAGE_ELEMENT["tp_button_off_en"])
        except:
            click(PAGE_ELEMENT["tp_button_off_id"])
    except:
        log.info(f"TP button OFF for {email_id} already")
    try:
        click(PAGE_ELEMENT["tp_button_done_en"])
    except:
        click(PAGE_ELEMENT["tp_button_done_id"])
    log.info("Done")

# Delete the profile
def delete_profile(email_id):
    log.info(f"Delete the profile {email_id}")
    open_link(PAGE_URL["url_dp"])
    time.sleep(2)
    clear_field(element=PAGE_ELEMENT["owner_profile_name"])
    clear_field(element=PAGE_ELEMENT["profile1_name"])
    clear_field(element=PAGE_ELEMENT["profile2_name"])
    clear_field(element=PAGE_ELEMENT["profile3_name"])
    clear_field(element=PAGE_ELEMENT["profile4_name"])
    filling(element=PAGE_ELEMENT["owner_profile_name"], fill="1")
    time.sleep(4)
    enter_key()
    open_link(PAGE_URL["url_dp"])
    time.sleep(2)
    clear_field(element=PAGE_ELEMENT["profile1_name"])
    clear_field(element=PAGE_ELEMENT["profile2_name"])
    clear_field(element=PAGE_ELEMENT["profile3_name"])
    clear_field(element=PAGE_ELEMENT["profile4_name"])
    filling(element=PAGE_ELEMENT["profile1_name"], fill="2")
    filling(element=PAGE_ELEMENT["profile2_name"], fill="3")
    filling(element=PAGE_ELEMENT["profile3_name"], fill="4")
    filling(element=PAGE_ELEMENT["profile4_name"], fill="5")
    time.sleep(4)
    enter_key()

# Remove the pin
def remove_pin(email_id, password):
    log.info("Remove the pin")
    open_link(PAGE_URL["url_rp"])
    time.sleep(3)
    log.info(f"{email_id} : parental password")
    filling(
        element=PAGE_ELEMENT["form_parental_control"], 
        fill=password
    )
    time.sleep(1)
    enter_key()
    time.sleep(2)
    try:
        click(PAGE_ELEMENT["checkbox_parental_control_en"])
    except:
        click(PAGE_ELEMENT["checkbox_parental_control_id"])
    time.sleep(1)
    try:
        click(PAGE_ELEMENT["applybutton_parental_control_en"])
    except:
        click(PAGE_ELEMENT["applybutton_parental_control_id"])

# Clean the history
def clean_history(email_id):
    log.info("Hide the history")
    open_link(PAGE_URL["url_ch"])
    time.sleep(3)
    # try:
    try:
        click(PAGE_ELEMENT["hide_all_history_button_en"])
    except:
        click(PAGE_ELEMENT["hide_all_history_button_id"])
    log.info(f"Hidden the history for {email_id}")
    time.sleep(2)
    try:
        click(PAGE_ELEMENT["confirm_delete_history_en"])
    except:
        click(PAGE_ELEMENT["confirm_delete_history_id"])
    time.sleep(1)

# Change the password
def change_password(email_id, password):
    new_password = NEW_PASS_LISTS[password]
    log.info(f"Change the password for {email_id}")
    log.info(f"New password : {new_password}")
    open_link(PAGE_URL["url_cp"])
    time.sleep(10)
    filling(
        element=PAGE_ELEMENT["cp_current_password"], 
        fill=password
    )
    time.sleep(1)
    filling(
        element=PAGE_ELEMENT["cp_new_password"], 
        fill=new_password
    )
    time.sleep(1)
    filling(
        element=PAGE_ELEMENT["cp_confirm_new_password"], 
        fill=new_password
    )
    time.sleep(1)
    enter_key()
    log.info(f"Changed the password for {email_id}")

# Clean the cookies
def clean_cookies(email_id):
    log.info("Clean the cookies")
    open_link(PAGE_URL["url_cc"])
    time.sleep(3)
    log.info(f"Cleaned the cookies for {email_id}")

# def get_account_information(email_id):
#     log.info(f"Get the account information for {email_id}")
#     open_link(PAGE_URL["url_ya"])
#     time.sleep(4)
#     # Payment metthod
#     try:
#         payment_method = get_text('//*[@id="appMountPoint"]/div/div/div/div[3]/div/div/div[5]/div[1]/section/div[2]/div/div/div[1]/div[1]')
#     except:
#         payment_method = get_text('//*[@id="appMountPoint"]/div/div/div/div[3]/div/div/div[5]/div[1]/section/div[2]/div/div/div[1]/div[2]')
#     # Due date
#     try:
#         due_date = get_text('//*[@id="appMountPoint"]/div/div/div/div[3]/div/div/div[5]/div[1]/section/div[2]/div/div/div[1]/div[2]')
#     except:
#         log.error("No due date")
#     print(payment_method, due_date)
#     return payment_method, due_date

def screenshot_account_information(email_id):
    log.info(f"Screenshot the account information for {email_id}")
    open_link(PAGE_URL["url_ya"])
    time.sleep(3)
    screenshot(name=f"hackback_{args.n}_{email_id}_{datetime.now()}")

# Flow of the scripts (Alur Jalannya Script)
# payment_method_list = []
# due_date_list = []
account_list = []
status_list = []
state_list = []
def flow():
    for _, i in CREDENTIAL_DF.iterrows():
        email_id = i["email"]
        password = i["pass"]

        # Setup the result file
        try:
            df_result = pd.DataFrame(
                {
                    "email" : account_list,
                    "status" : status_list,
                    "state" : state_list
                }
            )

            df_result.to_csv(
                f"results/hackback_{args.n}.csv"
            )
        except:
            pass
        account_list.append(email_id)
        driver_start()
        try:
            log.info(f"Start hackback for {email_id}")
            login(email_id, password) # Login to netflix
        except:
            log.error(f"FAILED LOGIN : {email_id}")
            status = "FAILED"
            state = "failed login"
            status_list.append(status)
            state_list.append(state)
            continue
        try:
            time.sleep(3)
            tp_off(email_id) # Turn off the TP
        except:
            log.error(f"FAILED to login : {email_id}")
            status = "FAILED"
            state = "failed to login"
            status_list.append(status)
            state_list.append(state)
            continue
        try:
            screenshot_account_information(email_id)
        except:
            log.error(f"FAILED screenshot the account information : {email_id}")
            status = "FAILED"
            state = "failed screenshot account information"
            status_list.append(status)
            state_list.append(state)
            continue
        try:
            time.sleep(3)
            delete_profile(email_id) # Delete the profile
        except:
            log.error(f"FAILED DELETE : {email_id}")
            status = "FAILED"
            state = "failed delete profile"
            status_list.append(status)
            state_list.append(state)
            continue
        try:
            time.sleep(3)
            remove_pin(email_id, password) # Remove the pin
        except:
            log.error(f"FAILED PIN : {email_id}")
            status = "FAILED"
            state = "failed remove pin"
            status_list.append(status)
            state_list.append(state)
            continue
        try:
            time.sleep(3)
            clean_history(email_id) # Clean the history
        except:
            log.error(f"Has Empty history : {email_id}")
            status = "Has Empty history"
            state = "Has Empty history"
            status_list.append(status)
            state_list.append(state)
            pass
        try:
            time.sleep(3)
            change_password(email_id, password) # Change the password
        except:
            log.error(f"FAILED PASSWORD : {email_id}")
            status = "FAILED"
            state = "failed change password"
            status_list.append(status)
            state_list.append(state)
            continue
        try:
            time.sleep(3)
            clean_cookies(email_id) # Clean the cookies
        except:
            log.error(f"FAILED CLEAN COOKIES : {email_id}")
            status = "FAILED"
            state = "failed clean cookies"
            status_list.append(status)
            state_list.append(state)
            continue
        
        account_list.append(email_id)
        try:
            status_list.append(status)
            state_list.append(state)
        except:
            status_list.append("SUCCESS")
        try:
            state_list.append(state)
        except:
            state_list.append("success")
        # try:
        #     payment_method_list.append(payment_method)
        # except:
        #     payment_method_list.append("Failed")
        # try:
        #     due_date_list.append(due_date)
        # except:
        #     due_date_list.append("Failed")

        close_driver() # Close the driver

        log.info(f"Done hackback for {email_id}")
if __name__ == "__main__":
    flow()