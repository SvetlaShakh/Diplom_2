import pytest
import allure
from api_stellar_burgers import StellarBurgersApi
import helpers
import data_stellar_burgers


class TestGetUsersOrders:

    @allure.title('Проверка успешного получения заказов пользователя - код ответа 200')
    @allure.description('При отправке запроса получения списка заказов пользователя с авторизацией'
                        'на ручку GET api/orders возвращается код ответа 200 с текстом: '
                        '"success": true, "orders": [], "total": "","totalToday": ""}')
    @pytest.mark.parametrize('count_burgers', data_stellar_burgers.list_count_burgers)
    def test_successful_get_users_orders(self, create_user, count_burgers):
        created_user = create_user
        token = created_user[1]
        list_ingredients = {'ingredients': helpers.generate_list_ingredients()}
        for i in range(count_burgers):
            StellarBurgersApi.create_order(token, list_ingredients)
        response = StellarBurgersApi.get_users_orders(token)
        list_errors = helpers.expected_body_response_successful_get_users_orders(response, count_burgers)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 200 and len(list_errors) == 0, f'body errors: {list_errors}'

    @allure.title('Проверка успешного получения заказов пользователя без заказов- код ответа 200')
    @allure.description('При отправке запроса получения списка заказов пользователя с авторизацией и без заказов'
                        'на ручку GET api/orders возвращается код ответа 200 с текстом: '
                        '"success": true, "orders": [], "total": 0,"totalToday": 0}')
    def test_successful_get_users_orders_whithout_orders(self, create_user):
        created_user = create_user
        token = created_user[1]
        response = StellarBurgersApi.get_users_orders(token)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 200 and response.json() == data_stellar_burgers.text_get_order_whithout_orders

    @allure.title('Проверка получения заказов пользователя без авторизации- код ответа 401')
    @allure.description('При отправке запроса получения списка заказов пользователя без авторизацией'
                        'на ручку GET api/orders возвращается код ответа 401 с текстом: '
                        '"success": False, "massage": "You should be authorised"')
    def test_get_users_orders_unauthorized(self, create_user):
        created_user = create_user
        token = created_user[1]
        list_ingredients = {'ingredients': helpers.generate_list_ingredients()}
        StellarBurgersApi.create_order(token, list_ingredients)
        response = StellarBurgersApi.get_users_orders(None)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 401 and response.json() == data_stellar_burgers.text_get_order_unauthorized
