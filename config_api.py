import requests
import jsonpath
import json
# from assertpy import assert_that
from ast import literal_eval
from random import randint

BASE_URL = "https://simple-books-api.glitch.me"


def get_api_status():
    response = requests.get(f"{BASE_URL}/status")

    json_response = json.loads(response.text)
    print(json_response)

    status_text = jsonpath.jsonpath(json_response, 'status')
    print(status_text[0])


def get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    json_response = json.loads(response.text)
    print(json_response)


def create_random_user_data():
    """Create a random user and save data in current_user_data.txt"""
    random = randint(0, 1000)  # range can be increase
    user = {
        "clientName": "Adrian",
        "clientEmail": f"adrianmacovei{random}@gmail.com"
    }
    with open('current_user_data.txt', 'w') as user_data:
        user_data.write(str(user))


def take_user_data():
    """Take current user data from current_user_data.txt and return it into dict/object format"""
    create_random_user_data()
    with open('current_user_data.txt', 'r') as user_data:
        user_data = literal_eval(user_data.read())
        return user_data


def api_authentication():
    """ If user is uniq save token in access_token.txt, else return json_return for testing purposes"""
    json_send_data = take_user_data()
    response = requests.post(url=f"{BASE_URL}/api-clients", json=json_send_data)
    json_response = json.loads(response.text)
    with open('access_token.txt', 'w') as access_token:
        if "accessToken" in json_response:
            access_token.write(response.text)
        else:
            print(json_response)
            return json_response


def get_access_token():
    """Returns the access token but before transform text from access_token.txt in dict, access value of key
    accessToken and save it in token_access variable"""

    with open('access_token.txt', 'r') as access_token:
        token_access = literal_eval(access_token.read())['accessToken']
        return token_access

api_authentication()
TOKEN = get_access_token()
print(TOKEN)
