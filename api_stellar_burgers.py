import allure
import requests
import urls


class StellarBurgersApi:

    @staticmethod
    @allure.step('Отправить запрос на создание пользователя POST api/auth/register')
    def registration_user(body):
        return requests.post(urls.BASE_URL + urls.REGISTER_USER, json=body)

    @staticmethod
    @allure.step('Отправить запрос на авторизацию пользователя POST api/auth/login')
    def login_user(body):
        return requests.post(urls.BASE_URL + urls.LOGIN_USER, json=body)

    @staticmethod
    @allure.step('Отправить запрос на изменение данных пользователя PATCH api/auth/user')
    def change_data_user(token, body):
        headers = {'Authorization': token}
        return requests.patch(urls.BASE_URL + urls.DATA_USER, headers=headers, json=body)

    @staticmethod
    @allure.step('Отправить запрос на удаление пользователя DELETE api/auth/user')
    def delete_user(token):
        headers = {'Authorization': token}
        return requests.delete(urls.BASE_URL + urls.DATA_USER, headers=headers)

    @staticmethod
    @allure.step('Отправить запрос на создание заказа POST api/orders')
    def create_order(token, body):
        headers = {'Authorization': token}
        return requests.post(urls.BASE_URL + urls.ORDER, headers=headers, json=body)

    @staticmethod
    @allure.step('Отправить запрос на получение заказов пользователя GET api/orders')
    def get_users_orders(token):
        headers = {'Authorization': token}
        return requests.get(urls.BASE_URL + urls.ORDER, headers=headers)

    @staticmethod
    @allure.step('Отправить запрос на получение игредиентов GET api/ingredients')
    def get_ingredients():
        return requests.get(urls.BASE_URL + urls.INGREDIENTS)
