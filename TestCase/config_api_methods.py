import requests
import json
from random import randint
from pathlib import Path

BASE_URL = "https://simple-books-api.glitch.me"
CURRENT_DIR = str(Path.cwd())
PATH_TO_ACCESS_TOKEN = (CURRENT_DIR + '\\access_token.txt').replace('\TestCase', "\\UserData")
PATH_TO_USER_DATA = (CURRENT_DIR + '\\current_user_data.txt').replace('\TestCase', "\\UserData")


def api_status():
    """Returns the request response for get api status"""
    response_status_api = requests.get(f"{BASE_URL}/status")
    return response_status_api


def get_all_books():
    """Returns the request response for get all books"""
    response_get_all_books = requests.get(f"{BASE_URL}/books")
    return response_get_all_books


def get_one_book(book_id):
    """Returns the request response for get one book by id"""
    response_get_one_book = requests.get(f"{BASE_URL}/books/{book_id}")
    return response_get_one_book


def get_filter_books(book_type, limit=10):
    """Returns the request response for get one books using filter like type and limit"""
    params = {
        "type": book_type,
        "limit": limit
    }
    response = requests.get(url=f"{BASE_URL}/books", params=params)
    return response  # json.loads(response.text)


def order_a_book(book_id):
    """Returns the request response for create a new order"""
    with open(PATH_TO_USER_DATA, "r") as customer_info:
        customer_name = json.load(customer_info)["clientName"]

    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()

    payload = {
        "bookId": book_id,
        "customerName": customer_name
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    response = requests.post(url=f'{BASE_URL}/orders', json=payload, headers=headers)
    return response


def get_all_orders():
    """Returns the request response for get all the orders"""
    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    response = requests.get(url=f'{BASE_URL}/orders', headers=headers)
    return response


def get_a_specific_order(order_id):
    """Returns the request response for get a specific order by id"""
    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()
    headers = {
        "Authorization": token,
    }

    response = requests.get(url=f'{BASE_URL}/orders/{order_id}', headers=headers)
    return response


def update_order_customer_name(order_id, new_name):
    """Returns the request response for update an order customer name"""
    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()
    headers = {
        "Authorization": token,
    }

    json_body = {
        "customerName": new_name,
    }
    response = requests.patch(url=f'{BASE_URL}/orders/{order_id}', headers=headers, json=json_body)
    return response


def delete_a_specific_order(order_id):
    """Returns the request response for delete an order by id"""
    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()
    headers = {
        "Authorization": token,
    }
    response = requests.delete(url=f'{BASE_URL}/orders/{order_id}', headers=headers)
    return response


def create_new_user_data():
    """Create a random user and save data in current_user_data.txt"""
    random = randint(0, 10000)  # range can be increase
    user = {
        "clientName": f"Adrian{random}",
        "clientEmail": f"adrianmacovei{random}@gmail.com"
    }
    with open(f'{PATH_TO_USER_DATA}', 'w') as user_data:
        json.dump(user, user_data, indent=4)


def take_user_data():
    """Take current user data from current_user_data.txt and return it into dict/object format"""
    with open(PATH_TO_USER_DATA, 'r') as user_data:
        return json.loads(user_data.read())


def api_authentication():
    """Save token in access_token.txt if user is new and return response, else return response for testing purposes"""
    response_api_auth = requests.post(url=f"{BASE_URL}/api-clients", json=take_user_data())
    json_response = json.loads(response_api_auth.text)
    if "accessToken" in json_response:
        with open(PATH_TO_ACCESS_TOKEN, 'w') as access_token:
            # if accessToken in json_response than save the value of token in access_token.txt in str format
            access_token.write(str(json_response["accessToken"]))
            return response_api_auth
    else:
        return response_api_auth


def get_access_token():
    """Return access token string value"""

    with open(PATH_TO_ACCESS_TOKEN, 'r') as access_token:
        token_access = access_token.read()
        return token_access


def delete_token():
    """Delete access token for testing purposes"""
    file = open(PATH_TO_ACCESS_TOKEN, 'w')
    file.close()


def change_order_data(order_id, param, new_param):
    """Returns the request response for patch/update order attribute"""
    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()
    headers = {
        "Authorization": token,
    }

    json_body = {
        param: new_param,
    }
    response = requests.patch(url=f'{BASE_URL}/orders/{order_id}', headers=headers, json=json_body)
    return response

def delete_a_book(book_id):
    """Try to delete book and return response"""
    response_delete_book = requests.delete(f"{BASE_URL}/books/{book_id}")
    return response_delete_book

def delete_all_orders():
    """Returns the request response for try to delete all orders"""
    with open(PATH_TO_ACCESS_TOKEN, "r") as access_token:
        token = access_token.read()
    headers = {
        "Authorization": token,
    }
    response = requests.delete(url=f'{BASE_URL}/orders', headers=headers)
    return response

def authenticate(client_name, client_email):
    json_data = {
        "clientName": client_name,
        "clientEmail": client_email,
    }
    response_api_auth = requests.post(url=f"{BASE_URL}/api-clients", json=json_data)
    return response_api_auth

def get_biggest_book_id():
    """Find the biggest id book and return it"""
    books = get_all_books().json()
    max_id = 0
    for book in books:
        if book['id'] > max_id:
            max_id = book['id']
    return max_id
