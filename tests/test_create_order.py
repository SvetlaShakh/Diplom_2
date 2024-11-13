import allure
from api_stellar_burgers import StellarBurgersApi
import helpers
import data_stellar_burgers


class TestCreateOrder:

    @allure.title('Проверка успешного создания заказа - код ответа 200')
    @allure.description('При отправке запроса создания заказа со списком ингредиентов и авторизацией на ручку '
                        'POST api/orders возвращается код ответа 200 с текстом: '
                        '"success": true, "name": "",  "order": {"number": ""}')
    def test_successful_create_order_with_user(self, create_user):
        created_user = create_user
        token = created_user[1]
        list_ingredients = {'ingredients': helpers.generate_list_ingredients()}
        response = StellarBurgersApi.create_order(token, list_ingredients)
        list_errors = helpers.expected_body_response_successful_create_order(response)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 200 and len(list_errors) == 0, f'body errors: {list_errors}'

    @allure.title('Проверка создания заказа без авторизации - код ответа 401')
    @allure.description('При отправке запроса создания заказа со списком ингредиентов и авторизацией на ручку '
                        'POST api/orders возвращается код ответа 401 с текстом: '
                        '"success": False, "message": "You should be authorised"')
    def test_create_order_without_user_unauthorized(self):
        list_ingredients = {'ingredients': helpers.generate_list_ingredients()}
        response = StellarBurgersApi.create_order(None, list_ingredients)
        assert (response.status_code == 401 and response.json() == data_stellar_burgers.text_create_order_unauthorized)

    @allure.title('Проверка создания заказа без списка ингредиентов - код ответа 400')
    @allure.description('При отправке запроса создания заказа без списка ингредиентов и с авторизацией на ручку '
                        'POST api/orders возвращается код ответа 400 с текстом: '
                        '"success": False, "message": "Ingredient ids must be provided"')
    def test_create_order_without_ingredients_bad_request(self, create_user):
        created_user = create_user
        token = created_user[1]
        response = StellarBurgersApi.create_order(token, None)
        StellarBurgersApi.delete_user(token)
        assert (response.status_code == 400
                and response.json() == data_stellar_burgers.text_create_order_bad_request)

    @allure.title('Проверка создания заказа с пустым списком ингредиентов - код ответа 400')
    @allure.description('При отправке запроса создания заказа с пустым списком ингредиентов и с авторизацией на ручку '
                        'POST api/orders возвращается код ответа 400 с текстом: '
                        '"success": False, "message": "Ingredient ids must be provided"')
    def test_create_order_with_empty_ingredients_bad_request(self, create_user):
        created_user = create_user
        token = created_user[1]
        response = StellarBurgersApi.create_order(token, data_stellar_burgers.list_without_ingredients)
        StellarBurgersApi.delete_user(token)
        assert (response.status_code == 400
                and response.json() == data_stellar_burgers.text_create_order_bad_request)

    @allure.title('Проверка создания заказа со списком ингредиентов с некорректным хеш ингредиентов - код ответа 500')
    @allure.description('При отправке запроса создания заказа cо списком ингредиентов с неккоректым хеш ингредиетов '
                        'и с авторизацией на ручку POST api/orders возвращается код ответа 500')
    def test_create_order_with_uncorrect_hash_ingredients_internal_server_error(self, create_user):
        created_user = create_user
        token = created_user[1]
        response = StellarBurgersApi.create_order(token, data_stellar_burgers.list_uncorrect_hash_ingredients)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 500
