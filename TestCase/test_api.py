from config_api import *
from assertpy import assert_that
from cerberus import Validator


class TestApi:
    BOOK_SCHEMA = dict(id={'type': 'integer'}, name={'type': 'string'}, type={'type': 'string'},
                       available={'type': 'boolean'})

    ORDER_SCHEMA = dict(id={'type': 'string'}, bookId={'type': "integer"}, customerName={'type': 'string'},
                        createdBy={'type': 'string'}, quantity={'type': 'integer'}, timestamp={'type': 'integer'})

    def test_api_initial_status(self):
        assert_that(api_status().status_code).is_equal_to(200)
        assert_that(api_status().json()['status']).is_equal_to('OK')

    def test_get_all_books_response(self):

        v = Validator(TestApi.BOOK_SCHEMA)

        assert_that(get_all_books().status_code).is_equal_to(200)
        assert_that(v.validate(get_all_books().json()[0])).is_equal_to(True)
        assert_that(get_all_books().json()[0]['name']).is_equal_to("The Russian")

    def test_get_filter_books_correct_parameters(self):

        v = Validator(TestApi.BOOK_SCHEMA)

        assert_that(get_filter_books("fiction").status_code).is_equal_to(200)
        assert_that(v.validate(get_filter_books("fiction").json()[0])).is_equal_to(True)

        book_type = ['fiction', 'non-fiction']
        for book_type in book_type:
            books = get_filter_books(book_type).json()
            for book in books:
                assert_that(book['type']).is_equal_to(book_type)

        assert_that(len(get_filter_books("fiction", 1).json())).is_equal_to(1)
        assert_that(len(get_filter_books("non-fiction", 2).json())).is_equal_to(2)

    def test_get_a_book_with_available_id(self):
        assert_that(get_one_book(1).status_code).is_equal_to(200)
        assert_that(get_one_book(2).json()).contains_key("current-stock", "price")

    def test_api_authentication_with_new_user_data(self):
        create_new_user_data()
        response = api_authentication()

        assert_that(response.status_code).is_equal_to(201)
        assert_that(response.json()).contains_key("accessToken")

    def test_order_an_available_book(self):
        all_books = get_all_books().json()
        for book in all_books:
            if book['available']:
                response = order_a_book(book['id'])
                assert_that(response.status_code).is_equal_to(201)
                assert_that(response.json()['created']).is_equal_to(True)

    def test_order_an_unavailable_book(self):
        response = order_a_book(2)
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()).contains_value('This book is not in stock. Try again later.')

    def test_get_all_orders(self):

        v = Validator(TestApi.ORDER_SCHEMA)

        orders = get_all_orders()
        assert_that(orders.status_code).is_equal_to(200)

        assert_that(v.validate(orders.json()[0])).is_equal_to(True)

    def test_get_one_order_by_id(self):
        v = Validator(TestApi.ORDER_SCHEMA)

        order_id = get_all_orders().json()[0]['id']
        order = get_a_specific_order(order_id)

        assert_that(order.status_code).is_equal_to(200)
        assert_that(v.validate(order.json())).is_equal_to(True)
        assert_that(order.json()['id']).is_equal_to(order_id)

    def test_update_order_customer(self):
        order_id = get_all_orders().json()[0]['id']
        new_name = "Someone"
        response = update_order_customer_name(order_id, new_name)

        assert_that(response.status_code).is_equal_to(204)
        assert_that(get_a_specific_order(order_id).json()['customerName']).is_equal_to(new_name)

        # suggestion for dev to improve API
        # assert_that(response.content).is_not_empty()

    def test_delete_an_order(self):
        order_id = get_all_orders().json()[0]['id']
        response = delete_a_specific_order(order_id)
        message = f'No order with id {order_id}.'

        assert_that(response.status_code).is_equal_to(204)
        assert_that(get_a_specific_order(order_id).json()).contains_value(message)

        # suggestion for dev to improve API
        # assert_that(response.content).is_not_empty()

    def test_api_authentication_with_already_used_user_data(self):
        response = api_authentication()
        assert_that(response.status_code).is_equal_to(409)
        assert_that(response.json()).contains_value('API client already registered. Try a different email.')

    def test_get_all_orders_no_auth_token(self):
        delete_token()
        orders = get_all_orders()
        assert_that(orders.status_code).is_equal_to(401)
        assert_that(orders.json()).contains_value('Invalid bearer token.')

    def test_update_order_no_auth_token(self):
        create_new_user_data()
        api_authentication()
        order_id = get_all_orders().json()
        new_name = "Someone"

        delete_token()
        response = update_order_customer_name(order_id, new_name)
        assert_that(response.status_code).is_equal_to(401)
        assert_that(response.json()).contains_value('Invalid bearer token.')

    def test_delete_an_order_no_auth_token(self):
        create_new_user_data()
        api_authentication()
        order_a_book(3)

        order_id = get_all_orders().json()[0]['id']

        delete_token()
        response = delete_a_specific_order(order_id)

        assert_that(response.status_code).is_equal_to(401)
        assert_that(response.json()).contains_value('Invalid bearer token.')

    def test_get_a_book_with_unavailable_id(self):
        book_id = 100
        response = get_one_book(book_id)
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()).contains_value(f'No book with id {book_id}')

    def test_get_filter_books_incorrect_parameters(self):
        assert_that(get_filter_books("something").status_code).is_equal_to(400)

    def test_order_an_nonexistent_book(self):
        create_new_user_data()
        api_authentication()

        response = order_a_book(75)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).contains_value('Invalid or missing bookId.')

    def test_change_order_id(self):
        new_id = "sds45353sda553454"
        order_id = get_all_orders().json()[0]['id']
        response = change_order_data(order_id, "id", new_id)

        if response.status_code < 205:
            assert_that(get_a_specific_order(new_id).json()).contains_key("id")
        elif 400 <= response.status_code < 405:
            assert_that(response.json()).contains_key('error')
        # this should receive a 4xx status, receive 204 no response, but the order with new_id can't be found

    def test_change_order_quantity(self):
        new_quantity = 4
        order_id = get_all_orders().json()[0]['id']
        response = change_order_data(order_id, "quantity", new_quantity)
        print(response.status_code)
        if response.status_code < 205:
            assert_that(get_a_specific_order(order_id).json()["quantity"]).is_equal_to(new_quantity)
        elif 400 <= response.status_code < 405:
            assert_that(response.json()).contains_key('error')
        # this should receive a 4xx status, receive 204 no response, but the order still have quantity 1

    def test_delete_an_already_deleted_order(self):
        order_id = get_all_orders().json()[0]['id']
        delete_a_specific_order(order_id)

        response = delete_a_specific_order(order_id)
        assert_that(response.status_code).is_equal_to(404)

    def test_delete_a_book(self):
        response = delete_a_book(2)
        assert_that(response.status_code).is_equal_to(404)

