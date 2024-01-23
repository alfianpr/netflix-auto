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
parser = argparse.ArgumentParser(
    description="Input the number of hackback credentials"
)
parser.add_argument(
    "-n", help="input the number"
)
args = parser.parse_args()
CREDENTIAL = f"hackback_login_{args.n}"
NEW_PASS = f"hackback_newpass_{args.n}"

# Load the requirements files
PAGE_URL = json.load(
    open("config/hackback_url.json")
)
PAGE_ELEMENT = json.load(
    open("config/hackback_element.json")
)
CREDENTIAL_LISTS = json.load(
    open(f"credential/{CREDENTIAL}.json")
)
NEW_PASS_LISTS = json.load(
    open(f"credential/{NEW_PASS}.json")
)

# Setup the driver
driver, action = driver_start()

# Login to the netflix
def login(email_id, password):
    open_link(PAGE_URL["url_tp"])
    log.info(f"Login to netflix {PAGE_URL['url_tp']}")
    time.sleep(2)
    filling(
        PAGE_ELEMENT["email_login"], email_id
    )
    log.info(f"Input email {email_id}")
    filling(
        PAGE_ELEMENT["password_login"], password
    )
    log.info(f"Input password {password}")
    enter_key()

def tp_on():
    open_link(PAGE_URL["url_tp"])
    try:
        log.info("Turn on the TP")
        click(PAGE_ELEMENT["tp_button_on"])
    except:
        log.info("TP button ON")
    click(PAGE_ELEMENT["tp_button_done"])
    log.info("Done")

def delete_profile(email_id, url):
    try:
        log.info(f"Delete the profile {email_id}")
        open_link(url)
        clear_field(
            element=PAGE_ELEMENT["owner_profile_name"]
        )
        clear_field(
            element=PAGE_ELEMENT["profile1_name"]
        )
        clear_field(
            element=PAGE_ELEMENT["profile2_name"]
        )
        clear_field(
            element=PAGE_ELEMENT["profile3_name"]
        )
        clear_field(
            element=PAGE_ELEMENT["profile4_name"]
        )
        filling(
            element=PAGE_ELEMENT["owner_profile_name"], fill="1"
        )
        time.sleep(1)
        enter_key()
        time.sleep(2)
        open_link(url)
        time.sleep(1)
        filling(
            element=PAGE_ELEMENT["profile1_name"], fill="2"
        )
        filling(
            element=PAGE_ELEMENT["profile2_name"], fill="3"
        )
        filling(
            element=PAGE_ELEMENT["profile3_name"], fill="4"
        )
        filling(
            element=PAGE_ELEMENT["profile4_name"], fill="5"
        )
        time.sleep(1)
        enter_key()
    except:
        log.error(f"error while deleting the profile {email_id}")


for email_id, password in CREDENTIAL_LISTS.items():
    login(email_id, password)
    time.sleep(2)
    tp_on()
    time.sleep(2)
    delete_profile(email_id, PAGE_URL["url_dp"])

