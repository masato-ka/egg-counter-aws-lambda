import os
import json
import logging
import requests

DEVICE_ID = os.environ['DEVICE_ID']
AUTH_URL = 'https://api.soracom.io/v1/auth'
DATA_GET_URL = 'https://api.soracom.io/v1/data/Device/{}?sort=desc&limit=1'.format(DEVICE_ID)
DATA_POST_URL = 'https://api.soracom.io/v1/devices/{}/publish'.format(DEVICE_ID)
X_DEVICE_SECRET = os.environ['X_DEVICE_SECRET'].replace('\\','') #TODO May be AWS env value '=' character espaced '/'
AUTH_KEY = os.environ['AUTH_KEY']
AUTH_KEY_ID = os.environ['AUTH_KEY_ID']

MAX_REMAINING = int(os.environ['MAX_REMAINING'])

logger = logging.getLogger()

#TODO to persistent of cash.
def auth_request():
    post_request_header = {'Content-Type':'application/json'}
    auth_payload = {'authKey': AUTH_KEY, 'authKeyId': AUTH_KEY_ID}
    secret = requests.post(AUTH_URL, headers = post_request_header, data=json.dumps(auth_payload)).json()
    return (secret['apiKey'], secret['token'])


def get_latest_remaining():
    api_key = ""; token = ""
    try:
        api_key,token = auth_request()
    except KeyError or AttributeError:
        logger.error("Failed authentication to soracom.")
        raise Exception
    get_requets_heders = {'X-Soracom-API-Key': api_key, 'X-Soracom-Token': token}
    result = requests.get(DATA_GET_URL, headers=get_requets_heders).json()
    latest_remaining = 0
    if len(result) > 0:
        try:
             raw_string = result[0]['content']
             latest_remaining = json.loads(raw_string)['remaining']
        except KeyError or AttributeError:
            logger.warning("harvest returned ignore message format. {}".format(result))
    return int(latest_remaining)

def persistent_remaining(remaining):
    post_request_header = {'x-device-secret':X_DEVICE_SECRET, 'Content-Type':'application/json'}
    persist_payload = {'remaining':remaining}
    result = requests.post(DATA_POST_URL, headers=post_request_header, data=json.dumps(persist_payload))
    logger.info(result)

def do_single_click_event():
    latest_remaining = get_latest_remaining()
    remaining = latest_remaining - 1 if latest_remaining > 0 else 0
    persistent_remaining(remaining)

def do_double_click_event():
    latest_remaining = get_latest_remaining()
    remaining = latest_remaining + 1 if latest_remaining < MAX_REMAINING else MAX_REMAINING
    persistent_remaining(remaining)

def do_long_click_event():
    persistent_remaining(MAX_REMAINING)

def lambda_handler(event, context):

    click_type = event['deviceEvent']['buttonClicked']['clickType']
    if click_type == "SINGLE":
        do_single_click_event()
        logger.info("Called single click event.")
    if click_type == "DOUBLE":
        do_double_click_event()
        logger.info("Called double click event.")
    if click_type == "LONG":
        do_long_click_event()
        logger.info("Called Long press event.")
    return {"result":"success"}

