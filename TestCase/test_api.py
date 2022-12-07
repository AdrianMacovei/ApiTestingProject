import pytest
from config_api_methods import *
from assertpy import assert_that
from cerberus import Validator


class TestApi:
    BOOK_SCHEMA = dict(id={'type': 'integer'}, name={'type': 'string'}, type={'type': 'string'},
                       available={'type': 'boolean'})

    ORDER_SCHEMA = dict(id={'type': 'string'}, bookId={'type': "integer"}, customerName={'type': 'string'},
                        createdBy={'type': 'string'}, quantity={'type': 'integer'}, timestamp={'type': 'integer'})

    @pytest.fixture
    def validate_book_schema(self):
        v = Validator(TestApi.BOOK_SCHEMA)
        return v.validate

    @pytest.fixture
    def validate_order_schema(self):
        v = Validator(TestApi.ORDER_SCHEMA)
        return v.validate

    @pytest.fixture
    def authenticate_with_new_data(self):
        create_new_user_data()
        api_authentication()

    @pytest.fixture
    def rollback_auth_token(self):
        token = get_access_token()
        yield
        with open(PATH_TO_ACCESS_TOKEN, 'w') as access_token:
            access_token.write(token)

    @pytest.fixture
    def make_orders(self):
        for _ in range(3):
            order_a_book(3)

    def test_api_initial_status(self):
        assert_that(api_status().status_code).is_equal_to(200)
        assert_that(api_status().json()['status']).is_equal_to('OK')

    def test_api_authentication_with_new_user_data(self):
        create_new_user_data()
        response = api_authentication()

        assert_that(response.status_code).is_equal_to(201)
        assert_that(response.json()).contains_key("accessToken")

    def test_get_all_books_response(self, validate_book_schema):
        response = get_all_books()
        print(response.json())
        assert_that(response.status_code).is_equal_to(200)
        assert_that(validate_book_schema(response.json()[0])).is_equal_to(True)
        assert_that(response.json()[0]['name']).is_equal_to("The Russian")

    testdata_acceptable_param = [
        ("fiction", 2),
        ("fiction", 1),
        ("non-fiction", 2),
        ("non-fiction", 1),
    ]

    @pytest.mark.parametrize("book_type, limit", testdata_acceptable_param)
    def test_get_filter_books_correct_parameters(self, validate_book_schema, book_type, limit):
        assert_that(get_filter_books(book_type).status_code).is_equal_to(200)
        assert_that(validate_book_schema(get_filter_books(book_type).json()[0])).is_equal_to(True)

        books = get_filter_books(book_type).json()
        for book in books:
            assert_that(book['type']).is_equal_to(book_type)

        assert_that(len(get_filter_books(book_type, limit).json())).is_equal_to(limit)
        assert_that(len(get_filter_books(book_type, limit).json())).is_equal_to(limit)

    testdata_get_book = [(1, 'The Russian'),
                         (2, 'Just as I Am'),
                         (3, 'The Vanishing Half'),
                         (4, 'The Midnight Library'),
                         (5, 'Untamed'),
                         (6, 'Viscount Who Loved Me'),
                         ]

    @pytest.mark.parametrize("book_id, book_name", testdata_get_book)
    def test_get_a_book_with_available_id(self, book_id, book_name):
        response = get_one_book(book_id)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).contains_key("current-stock", "price")
        assert_that(response.json()["id"]).is_equal_to(book_id)
        assert_that(response.json()["name"]).is_equal_to(book_name)

    def test_order_available_book(self):
        all_books = get_all_books().json()
        for book in all_books:
            if book['available']:
                response = order_a_book(book['id'])
                assert_that(response.status_code).is_equal_to(201)
                assert_that(response.json()['created']).is_equal_to(True)

    def test_order_an_unavailable_book(self):
        all_books = get_all_books().json()
        response_order = None
        for book in all_books:
            if not book["available"]:
                response_order = order_a_book(book["id"])
                break
        assert_that(response_order.status_code).is_equal_to(404)
        assert_that(response_order.json()).contains_value('This book is not in stock. Try again later.')

    def test_get_all_orders(self, validate_order_schema):
        orders = get_all_orders()
        assert_that(orders.status_code).is_equal_to(200)
        assert_that(validate_order_schema(orders.json()[0])).is_equal_to(True)

    def test_get_one_order_by_id(self, validate_order_schema):
        order_id = get_all_orders().json()[0]['id']
        order = get_a_specific_order(order_id)

        assert_that(order.status_code).is_equal_to(200)
        assert_that(validate_order_schema(order.json())).is_equal_to(True)
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

    def test_get_a_book_with_unavailable_id(self):
        book_id = get_biggest_book_id() + 1
        response = get_one_book(book_id)
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()).contains_value(f'No book with id {book_id}')

    def test_get_filter_books_incorrect_type_parameter(self):
        assert_that(get_filter_books("something").status_code).is_equal_to(400)
    limit_param_data = [
                ("fiction", "something"),
                ("fiction", -1),
                ("non-fiction", 0)
            ]

    @pytest.mark.parametrize("book_type, limit", limit_param_data)
    def test_get_filter_books_invalid_data_in_limit_param(self, book_type, limit):
        response = get_filter_books(book_type, limit)
        if limit == 0 and response.status_code == 200:
            assert_that(response.json()).is_empty()
        assert_that(response.status_code).is_equal_to(400)
        # limit param accept string format and should not, accept value 0 but return all books available

    def test_order_an_nonexistent_book(self):
        response = order_a_book(get_biggest_book_id() + 1)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).contains_value('Invalid or missing bookId.')

    def test_try_change_order_id(self, make_orders):
        new_id = "sds45353sda553454"
        order_id = get_all_orders().json()[0]['id']
        response = change_order_data(order_id, "id", new_id)
        if response.status_code < 205:
            assert_that(get_a_specific_order(new_id).json()).contains_value("sds45353sda553454")
        elif 400 <= response.status_code < 405:
            assert_that(response.json()).contains_key('error')
        # this should receive a 4xx status, receive 204 no response, but the order with new_id can't be found

    def test_try_change_order_quantity(self, make_orders):
        new_quantity = 4
        order_id = get_all_orders().json()[0]['id']
        response = change_order_data(order_id, "quantity", new_quantity)
        print(response.status_code)
        if response.status_code < 205:
            assert_that(get_a_specific_order(order_id).json()["quantity"]).is_equal_to(new_quantity)
        elif 400 <= response.status_code < 405:
            assert_that(response.json()).contains_key('error')
        # this should receive a 4xx status, receive 204 no response, but the order still have quantity 1

    def test_delete_an_already_deleted_order(self, make_orders):
        order_id = get_all_orders().json()[0]['id']
        delete_a_specific_order(order_id)
        response = delete_a_specific_order(order_id)

        assert_that(response.status_code).is_equal_to(404)

    def test_try_delete_a_book(self):
        response = delete_a_book(2)
        assert_that(response.status_code).is_equal_to(404)

    def test_order_a_book_more_than_available_number(self):
        book_stock = get_one_book(1).json()["current-stock"]
        current_number_of_orders = len(get_all_orders().json())

        for _ in range(1, book_stock + 1):
            order_a_book(1)

        response = order_a_book(1)
        assert_that(len(get_all_orders().json())).is_equal_to(current_number_of_orders + book_stock + 1)
        assert_that(get_one_book(1).json()["current-stock"]).is_equal_to(0)
        assert_that(response.json()).contains_key("error")
        # no change in current-stock when order books and when the current stock is exceeded no error appears

    def test_try_delete_all_orders(self):
        response = delete_all_orders()
        assert_that(response.status_code).is_equal_to(404)

    def test_authentication_with_invalid_email_format(self):
        resp = authenticate("Bogdan", "sfsdafsa")

        assert_that(resp.status_code).is_equal_to(400)
        assert_that(resp.json()).contains_value('Invalid or missing client email.')

    def test_authentication_with_number_value_in_name(self):
        random = randint(0, 10000)
        resp = authenticate(3424, f"something{random}@gmail.com")
        assert_that(resp.status_code).is_equal_to(400)
        # name should be only string format but accept integer format too

    def test_get_all_orders_no_auth_token(self, rollback_auth_token):
        delete_token()
        orders = get_all_orders()
        assert_that(orders.status_code).is_equal_to(401)
        assert_that(orders.json()).contains_value('Invalid bearer token.')

    def test_update_order_no_auth_token(self, rollback_auth_token):
        order_id = get_all_orders().json()[0]['id']
        new_name = "Someone"
        delete_token()
        response = update_order_customer_name(order_id, new_name)
        assert_that(response.status_code).is_equal_to(401)
        assert_that(response.json()).contains_value('Invalid bearer token.')

    def test_delete_an_order_no_auth_token(self, rollback_auth_token):
        order_id = get_all_orders().json()[0]['id']
        delete_token()
        response = delete_a_specific_order(order_id)

        assert_that(response.status_code).is_equal_to(401)
        assert_that(response.json()).contains_value('Invalid bearer token.')

    def test_api_authentication_with_already_used_user_data(self):
        response = api_authentication()
        assert_that(response.status_code).is_equal_to(409)
        assert_that(response.json()).contains_value('API client already registered. Try a different email.')
