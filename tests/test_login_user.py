import pytest
import allure
from api_stellar_burgers import StellarBurgersApi
import helpers
import data_stellar_burgers


class TestLoginUser:

    @allure.title('Проверка успешного входа пользователя - код ответа 200')
    @allure.description('При отправке запроса входа пользователя с указанием данных email, password в теле '
                        'запроса на ручку POST /api/auth/login возвращается код ответа 200 с текстом: '
                        '"success": true, "user": {"email": "","name": ""},'
                        '"accessToken": "Bearer ...","refreshToken": ""}')
    def test_successful_login_user(self, create_user):
        created_user = create_user
        data_user = helpers.generate_data_user_two_parameters('email', 'name', created_user[0])
        login_data = helpers.generate_data_user_two_parameters('email', 'password', created_user[0])
        token = created_user[1]
        response = StellarBurgersApi.login_user(login_data)
        list_errors = helpers.expected_body_response_successful_login(response, data_user)
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 200 and len(list_errors) == 0, f'body errors: {list_errors}'

    @allure.title('Проверка входа пользователя c несуществующим email или password, или без указания одного из '
                  'параметров код ответа 401')
    @allure.description('При отправке запроса входа пользователя с указанием несуществующего email или password, '
                        'или без указания одного из параметров в теле запроса на ручку POST /api/auth/login '
                        'возвращается код ответа 401 с текстом: "email or password are incorrect"')
    @pytest.mark.parametrize('parm_1, parm_2', data_stellar_burgers.login_data_unauthorized)
    def test_one_parameter_login_user_unauthorized(self, create_user, parm_1, parm_2):
        created_user = create_user
        login_data = helpers.login_data_unauthorized(parm_1, parm_2, created_user[0])
        token = created_user[1]
        response = StellarBurgersApi.login_user(login_data)
        StellarBurgersApi.delete_user(token)
        assert (response.status_code == 401 and response.json() == data_stellar_burgers.text_login_user_unauthorized)
