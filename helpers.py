import random
import string
import allure
from api_stellar_burgers import StellarBurgersApi
import data_stellar_burgers


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.step('Создать словарь с данными для регистрации пользователя')
def generate_registration_body(length):
    registration_body = {}
    registration_body['email'] = f'{generate_random_string(length)}@mail.com'
    registration_body['password'] = generate_random_string(length)
    registration_body['name'] = generate_random_string(length)
    return registration_body


@allure.step('Создать словарь с ошибками тела ответа при регистрации пользователя')
def expected_body_response_successful_registration(response, data_user):
    list_errors = []
    not_expected_keys = []

    if 'success' not in response.json():
        list_errors.append('the key "success" is missing from the response body')
    elif response.json()['success'] != True:
        list_errors.append(f'expected "success" is True, actual {response.json()['success']}')

    if 'user' not in response.json():
        list_errors.append('the key "user" is missing from the response body')
    elif 'email' not in response.json()['user']:
        list_errors.append('the key "email" is missing from the response body/user')
    elif response.json()['user']['email'] != data_user['email']:
        list_errors.append(f'expected "user/email" is {data_user['email']}, actual {response.json()['user']['email']}')
    elif 'name' not in response.json()['user']:
        list_errors.append('the key "name" is missing from the response body/user')
    elif response.json()['user']['name'] != data_user['name']:
        list_errors.append(f'expected "user/name" is {data_user['name']}, actual {response.json()['user']['name']}')
    elif len(response.json()['user']) > len(data_stellar_burgers.key_registration_user):
        for key in response.json()['user']:
            if key not in data_stellar_burgers.key_registration_user:
                not_expected_keys.append(f'user/{key}')

    if 'accessToken' not in response.json():
        list_errors.append('the key "accessToken" is missing from the response body')

    if 'refreshToken' not in response.json():
        list_errors.append('the key "refreshToken" is missing from the response body')

    if len(response.json()) > len(data_stellar_burgers.expected_keys_successful_registration_user):
        for key in response.json():
            if key not in data_stellar_burgers.expected_keys_successful_registration_user:
                not_expected_keys.append(f'user/{key}')

    if len(not_expected_keys) > 0:
        list_errors.append(f'not expected keys: {not_expected_keys}')

    return list_errors


@allure.step('Создать словарь с данными пользователя - 2 параметра')
def generate_data_user_two_parameters(parm_1, parm_2, registration_body):
    registration_body_two_parameters = {}
    registration_body_two_parameters[parm_1] = registration_body[parm_1]
    registration_body_two_parameters[parm_2] = registration_body[parm_2]
    return registration_body_two_parameters

@allure.step('Создать словарь с данными для авторизации - 1 существующий параметр')
def login_data_unauthorized (parm_1, parm_2, registration_body):
    login_data = {}

    if parm_1 == 'email_true':
        login_data['email'] = registration_body['email']
    elif parm_1 == 'email_false':
        login_data['email'] = f'aa{registration_body['email']}'
    else:
        print('parm_1 has value ' + parm_1)

    if parm_2 == 'password_true':
        login_data['password'] = registration_body['password']
    elif parm_2 == 'password_false':
        login_data['password'] = f'aa{registration_body['password']}'
    else:
        print('parm_2 has value ' + parm_2)

    return login_data

@allure.step('Создать словарь с ошибками тела ответа при авторизации пользователя')
def expected_body_response_successful_login(response, data_user):
    list_errors = []
    not_expected_keys = []

    if 'success' not in response.json():
        list_errors.append('the key "success" is missing from the response body')
    elif response.json()['success'] != True:
        list_errors.append(f'expected "success" is True, actual {response.json()['success']}')

    if 'user' not in response.json():
        list_errors.append('the key "user" is missing from the response body')
    elif 'email' not in response.json()['user']:
        list_errors.append('the key "email" is missing from the response body/user')
    elif response.json()['user']['email'] != data_user['email']:
        list_errors.append(f'expected "user/email" is {data_user['email']}, actual {response.json()['user']['email']}')
    elif 'name' not in response.json()['user']:
        list_errors.append('the key "name" is missing from the response body/user')
    elif response.json()['user']['name'] != data_user['name']:
        list_errors.append(f'expected "user/name" is {data_user['name']}, actual {response.json()['user']['name']}')
    elif len(response.json()['user']) > len(data_stellar_burgers.key_login_user):
        for key in response.json()['user']:
            if key not in data_stellar_burgers.key_login_user:
                not_expected_keys.append(f'user/{key}')

    if 'accessToken' not in response.json():
        list_errors.append('the key "accessToken" is missing from the response body')

    if 'refreshToken' not in response.json():
        list_errors.append('the key "refreshToken" is missing from the response body')

    if len(response.json()) > len(data_stellar_burgers.expected_keys_successful_login_user):
        for key in response.json():
            if key not in data_stellar_burgers.expected_keys_successful_login_user:
                not_expected_keys.append(f'user/{key}')

    if len(not_expected_keys) > 0:
        list_errors.append(f'not expected keys: {not_expected_keys}')

    return list_errors

@allure.step('Создать словарь с новыми данными пользователя')
def generate_new_data_user (parm_1, parm_2, registration_body):
    new_data_user = {}
    expected_data_user = {}
    expected_data_user['email'] = registration_body['email']
    expected_data_user['name'] = registration_body['name']

    if parm_1 == 'email':
        new_data_user['email'] = registration_body['email']
    elif parm_1 == 'email_new':
        new_data_user['email'] = f'{generate_random_string(6)}@mail.com'
        expected_data_user['email'] = new_data_user['email']
    else:
        print('parm_1 has value ' + parm_1)

    if parm_2 == 'name':
        new_data_user['name'] = registration_body['name']
    elif parm_2 == 'name_new':
        new_data_user['name'] = generate_random_string(6)
        expected_data_user['name'] = new_data_user['name']
    else:
        print('parm_2 has value ' + parm_2)

    return new_data_user, expected_data_user

@allure.step('Создать словарь с новыми данными пользователя - email другого пользователя')
def generate_new_data_user_exists_email(registration_body_1, registration_body_2):
    new_data_user = {}
    new_data_user['email'] = registration_body_1['email']
    new_data_user['name'] = registration_body_2['name']
    return new_data_user

@allure.step('Создать словарь с ошибками тела ответа при изменении данных пользователя')
def expected_body_response_successful_change_data(response, data_user):
    list_errors = []
    not_expected_keys = []

    if 'success' not in response.json():
        list_errors.append('the key "success" is missing from the response body')
    elif response.json()['success'] != True:
        list_errors.append(f'expected "success" is True, actual {response.json()['success']}')

    if 'user' not in response.json():
        list_errors.append('the key "user" is missing from the response body')
    elif 'email' not in response.json()['user']:
        list_errors.append('the key "email" is missing from the response body/user')
    elif response.json()['user']['email'] != data_user['email']:
        list_errors.append(f'expected "user/email" is {data_user['email']}, actual {response.json()['user']['email']}')
    elif 'name' not in response.json()['user']:
        list_errors.append('the key "name" is missing from the response body/user')
    elif response.json()['user']['name'] != data_user['name']:
        list_errors.append(f'expected "user/name" is {data_user['name']}, actual {response.json()['user']['name']}')
    elif len(response.json()['user']) > len(data_stellar_burgers.key_change_user):
        for key in response.json()['user']:
            if key not in data_stellar_burgers.key_change_user:
                not_expected_keys.append(f'user/{key}')

    if len(response.json()) > len(data_stellar_burgers.expected_keys_successful_change_data_user):
        for key in response.json():
            if key not in data_stellar_burgers.expected_keys_successful_change_data_user:
                not_expected_keys.append(f'user/{key}')

    if len(not_expected_keys) > 0:
        list_errors.append(f'not expected keys: {not_expected_keys}')

    return list_errors

@allure.step('Создать список ингредиентов для заказа')
def generate_list_ingredients():
    list_ingredients = []
    response = StellarBurgersApi.get_ingredients()
    list_ingredients.append(response.json()['data'][0]['_id'])
    list_ingredients.append(response.json()['data'][3]['_id'])
    list_ingredients.append(response.json()['data'][6]['_id'])
    list_ingredients.append(response.json()['data'][11]['_id'])
    return list_ingredients

@allure.step('Создать словарь с ошибками тела ответа при создании заказа')
def expected_body_response_successful_create_order(response):
    list_errors = []
    not_expected_keys = []

    if 'success' not in response.json():
        list_errors.append('the key "success" is missing from the response body')
    elif response.json()['success'] != True:
        list_errors.append(f'expected "success" is True, actual {response.json()['success']}')

    if 'name' not in response.json():
        list_errors.append('the key "name" is missing from the response body')

    if 'order' not in response.json():
        list_errors.append('the key "user" is missing from the response body')
    elif len(response.json()['order']) > len(data_stellar_burgers.key_create_order):
        for key in response.json()['order']:
            if key not in data_stellar_burgers.key_create_order:
                not_expected_keys.append(f'order/{key}')

    if len(response.json()) > len(data_stellar_burgers.expected_keys_successful_create_order):
        for key in response.json():
            if key not in data_stellar_burgers.expected_keys_successful_create_order:
                not_expected_keys.append(f'user/{key}')

    if len(not_expected_keys) > 0:
        list_errors.append(f'not expected keys: {not_expected_keys}')

    return list_errors

@allure.step('Создать словарь с ошибками тела ответа при получении списка заказов пользователя')
def expected_body_response_successful_get_users_orders(response, count_burgers):
    list_errors = []
    not_expected_keys = []

    if 'success' not in response.json():
        list_errors.append('the key "success" is missing from the response body')
    elif response.json()['success'] != True:
        list_errors.append(f'expected "success" is True, actual {response.json()['success']}')

    if 'orders' not in response.json():
        list_errors.append('the key "user" is missing from the response body')
    elif 'ingredients' not in response.json()['orders'][0]:
        list_errors.append('the key "ingredients" is missing from the response body/orders')
    elif type(response.json()['orders'][0]['ingredients']) != list:
        list_errors.append(f'expected type "ingredients" is list, '
                           f'actual {type(response.json()['orders']['ingredients'])}')
    elif '_id' not in response.json()['orders'][0]:
        list_errors.append('the key "_id" is missing from the response body/orders')
    elif 'status' not in response.json()['orders'][0]:
        list_errors.append('the key "status" is missing from the response body/orders')
    elif response.json()['orders'][0]['status'] not in data_stellar_burgers.list_status_orders:
        list_errors.append(f'{response.json()['orders'][0]['status']} is not expected value of "status"')
    elif 'number' not in response.json()['orders'][0]:
        list_errors.append('the key "number" is missing from the response body/orders')
    elif 'createdAt' not in response.json()['orders'][0]:
        list_errors.append('the key "createdAt" is missing from the response body/orders')
    elif 'updatedAt' not in response.json()['orders'][0]:
        list_errors.append('the key "updatedAt" is missing from the response body/orders')
    elif len(response.json()['orders'][0]) > len(data_stellar_burgers.keys_get_orders):
        for key in response.json()['orders'][0]:
            if key not in data_stellar_burgers.keys_get_orders:
                not_expected_keys.append(f'orders/{key}')

    elif count_burgers > len(response.json()['orders']) < 51 :
        list_errors.append(f'Not all orders are displayed, '
                           f'expected: {count_burgers}, actual:{len(response.json()['orders'])}')
    elif len(response.json()['orders']) > 51 < count_burgers:
        list_errors.append(f'count orders are displayed expected: 50, actual:{len(response.json()['orders'])}')

    if 'totalToday' not in response.json():
        list_errors.append('the key "totalToday" is missing from the response body')
    elif response.json()['totalToday'] != count_burgers:
        list_errors.append(f'"totalToday" expected: {count_burgers}, actual:{response.json()['totalToday']}')

    if 'total' not in response.json():
        list_errors.append('the key "total" is missing from the response body')
    elif response.json()['total'] < count_burgers:
        list_errors.append(f'"total" expected: more then {count_burgers}, actual:{response.json()['total']}')

    if len(response.json()) > len(data_stellar_burgers.expected_keys_successful_get_users_orders):
        for key in response.json():
            if key not in data_stellar_burgers.expected_keys_successful_get_users_orders:
                not_expected_keys.append(f'user/{key}')


    if len(not_expected_keys) > 0:
        list_errors.append(f'not expected keys: {not_expected_keys}')

    return list_errors
