from netlib.utils import (
    open_link,
    driver_start,
    log,
    filling,
    enter_key,
    click,
    clear_field
)
import json
import argparse
import pandas as pd
import time

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

# Setup the driver
driver, action = driver_start()

# Login to the netflix
def login(email_id, password):
    try:
        open_link(PAGE_URL["url_tp"])
        log.info(f"Login to netflix {PAGE_URL['url_tp']}")
        time.sleep(7)
        filling(PAGE_ELEMENT["email_login"], email_id)
        log.info(f"Input email {email_id}")
        filling(PAGE_ELEMENT["password_login"], password)
        log.info(f"Input password {password}")
        enter_key()
    except:
        log.error(f"Cant login to netflix {email_id}")

# Turn off the TP
def tp_off(email_id):
    try:
        try:
            log.info(f"Turn on the TP for {email_id}")
            try:
                click(PAGE_ELEMENT["tp_button_on_en"])
            except:
                click(PAGE_ELEMENT["tp_button_on_id"])
        except:
            log.info(f"TP button ON for {email_id} already")
        try:
            click(PAGE_ELEMENT["tp_button_done_en"])
        except:
            click(PAGE_ELEMENT["tp_button_done_id"])
        log.info("Done")
    except:
        log.error(f"INCORRECT PASSWORD : {email_id}")

# Delete the profile
def delete_profile(email_id):
    try:
        log.info(f"Delete the profile {email_id}")
        open_link(PAGE_URL["url_dp"])
        time.sleep(2)
        clear_field(element=PAGE_ELEMENT["owner_profile_name"])
        clear_field(element=PAGE_ELEMENT["profile1_name"])
        clear_field(element=PAGE_ELEMENT["profile2_name"])
        clear_field(element=PAGE_ELEMENT["profile3_name"])
        clear_field(element=PAGE_ELEMENT["profile4_name"])
        filling(element=PAGE_ELEMENT["owner_profile_name"], fill="1")
        time.sleep(3)
        enter_key()
        open_link(PAGE_URL["url_dp"])
        time.sleep(2)
        filling(element=PAGE_ELEMENT["profile1_name"], fill="2")
        filling(element=PAGE_ELEMENT["profile2_name"], fill="3")
        filling(element=PAGE_ELEMENT["profile3_name"], fill="4")
        filling(element=PAGE_ELEMENT["profile4_name"], fill="5")
        time.sleep(4)
        enter_key()
    except:
        log.info(f"{email_id} already deleted")

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
    try:
        try:
            click(PAGE_ELEMENT["hide_all_history_button_en"])
        except:
            click(PAGE_ELEMENT["hide_all_history_button_id"])
        log.info(f"Hidden the history for {email_id}")
    except:
        log.info(f"{email_id} already hidden")

# Change the password
def change_password(email_id, password):
    new_password = NEW_PASS_LISTS[password]
    log.info(f"Change the password for {email_id}")
    open_link(PAGE_URL["url_cp"])
    time.sleep(3)
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

# Flow of the scripts
def flow():
    for _, i in CREDENTIAL_DF.iterrows():
        email_id = i["email"]
        password = i["pass"]

        log.info(f"Start hackback for {email_id}")
        login(email_id, password)
        time.sleep(3)
        tp_off(email_id)
        time.sleep(3)
        delete_profile(email_id)
        time.sleep(3)
        remove_pin(email_id, password)
        time.sleep(3)
        clean_history(email_id)
        time.sleep(3)
        change_password(email_id, password)
        time.sleep(4)
        clean_cookies(email_id)

if __name__ == "__main__":
    flow()