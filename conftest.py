import pytest
import allure
from api_stellar_burgers import StellarBurgersApi
import helpers

@pytest.fixture()
def create_user():
    registration_body = helpers.generate_registration_body(6)
    response = StellarBurgersApi.registration_user(registration_body)
    token = response.json()['accessToken']
    return registration_body, token