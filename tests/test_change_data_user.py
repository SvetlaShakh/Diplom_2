import pytest
import allure
from api_stellar_burgers import StellarBurgersApi
import helpers
import data_stellar_burgers


class TestChangeDataUser:

    @allure.title('Проверка изменения данных пользователя - код ответа 200')
    @allure.description('При отправке запроса на изменения данных пользователя с изменениям одного из параметров '
                        'email или name в теле запроса на ручку PATCH /api/auth/user возвращается код ответа 200 '
                        'с текстом: "success": true, "user": {"email": "","name": ""}')
    @pytest.mark.parametrize('parm_1, parm_2', data_stellar_burgers.list_new_data_user)
    def test_successful_change_data_user(self, create_user, parm_1, parm_2):
        created_user = create_user
        new_data_user = helpers.generate_new_data_user(parm_1, parm_2, created_user[0])
        token = created_user[1]
        response = StellarBurgersApi.change_data_user(token, new_data_user[0])
        list_errors = helpers.expected_body_response_successful_change_data(response, new_data_user[1])
        StellarBurgersApi.delete_user(token)
        assert response.status_code == 200 and len(list_errors) == 0, f'body errors: {list_errors}'

    @allure.title('Проверка изменения данных пользователя без авторизации - код ответа 401')
    @allure.description('При отправке запроса на изменения данных пользователя с изменениям одного из параметров email '
                        'или name в теле запроса  без авторизации на ручку PATCH /api/auth/user возвращается '
                        'код ответа 401 с текстом: "success": False, "massage": "You should be authorised"')
    @pytest.mark.parametrize('parm_1, parm_2', data_stellar_burgers.list_new_data_user)
    def test_change_data_user_unauthorized(self, create_user, parm_1, parm_2):
        created_user = create_user
        new_data_user = helpers.generate_new_data_user(parm_1, parm_2, created_user[0])
        token = created_user[1]
        response = StellarBurgersApi.change_data_user(None, new_data_user[0])
        StellarBurgersApi.delete_user(token)
        assert (response.status_code == 401
                and response.json() == data_stellar_burgers.text_change_data_user_unauthorized)

    @allure.title('Проверка изменения данных пользователя email на email другого пользователя - код ответа 403')
    @allure.description('При отправке запроса на изменения данных пользователя с изменениям одного из параметров '
                        'email или name в теле запроса на ручку PATCH /api/auth/user возвращается код ответа 200 '
                        'с текстом: "success": true, "massage": "You should be authorised"')
    def test_change_data_user_exists_email_forbidden(self, create_user):
        created_user = create_user
        registration_body_2 = helpers.generate_registration_body(5)
        response_2 = StellarBurgersApi.registration_user(registration_body_2)
        new_data_user_2 = helpers.generate_new_data_user_exists_email(created_user[0], registration_body_2)
        token_1 = created_user[1]
        token_2 = response_2.json()['accessToken']
        response = StellarBurgersApi.change_data_user(token_2, new_data_user_2)
        StellarBurgersApi.delete_user(token_1)
        StellarBurgersApi.delete_user(token_2)
        assert (response.status_code == 403
                and response.json() == data_stellar_burgers.text_change_data_user_forbidden)
