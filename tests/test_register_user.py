import pytest
import allure
from api_stellar_burgers import StellarBurgersApi
import helpers
import data_stellar_burgers


class TestRegisterUser:

    @allure.title('Проверка успешного создания пользователя - код ответа 200')
    @allure.description('При отправке запроса создания пользователя с указанием данных email, name, password в теле '
                        'запроса на ручку POST /api/auth/register возвращается код ответа 200 с текстом: '
                        '"success": true, "user": {"email": "","name": ""},'
                        '"accessToken": "Bearer ...","refreshToken": ""}')
    def test_successful_registration_user(self):
        registration_body = helpers.generate_registration_body(6)
        data_user = helpers.generate_data_user_two_parameters('email', 'name', registration_body)
        response = StellarBurgersApi.registration_user(registration_body)
        token = response.json()['accessToken']
        list_errors = helpers.expected_body_response_successful_registration(response, data_user)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 200 and len(list_errors) == 0, f'body errors: {list_errors}'

    @allure.title('Проверка создания пользователя c данными существующего пользователя - код ответа 403')
    @allure.description('При отправке запроса создания пользователя с указанием данных email, name, password '
                        'ранее созданного пользователя в теле запроса на ручку POST /api/auth/register возвращается '
                        'код ответа 403 с текстом: '
                        '{"success": False, "message": "User already exists"}')
    def test_registration_same_user_forbidden(self):
        registration_body = helpers.generate_registration_body(6)
        response = StellarBurgersApi.registration_user(registration_body)
        token = response.json()['accessToken']
        response = StellarBurgersApi.registration_user(registration_body)
        StellarBurgersApi.delete_user(token)
        assert (response.status_code == 403 and response.json() == data_stellar_burgers.text_registration_same_user)

    @allure.title('Проверка создания пользователя без указания одного из параметра - код ответа 403')
    @allure.description('При отправке запроса создания пользователя без указания данных одного из параметров '
                        'email, name, password в теле запроса на ручку POST /api/auth/register возвращается '
                        'код ответа 403 с текстом: '
                        '{"success": False, "message": "Email, password and name are required fields"}')
    @pytest.mark.parametrize('parm_1, parm_2', data_stellar_burgers.parameters_list)
    def test_registration_two_parameters_user_forbidden(self, parm_1, parm_2):
        registration_body = helpers.generate_registration_body(6)
        registration_body_two_parameters = helpers.generate_data_user_two_parameters(parm_1, parm_2, registration_body)
        response = StellarBurgersApi.registration_user(registration_body_two_parameters)
        assert (response.status_code == 403
                and response.json() == data_stellar_burgers.text_registration_user_two_param)
