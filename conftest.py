import allure
import pytest
import requests
from src.config import Config
from src.helpers import generate_random_user

@pytest.fixture
@allure.description('Создание нового пользователя')
def create_user():
    user_data = generate_random_user()
    response = requests.post(f'{Config.URL}api/auth/register', json=user_data)
    r = response.json()
    assert response.status_code == 200, f'Ожидается статус: 200, получен статус: {response.status_code}'
    token = r.get('accessToken')
    yield {'user_data': user_data, 'token': token}
    requests.delete(f'{Config.URL}api/auth/user', headers={'Authorization': f'Bearer {token}'})

@pytest.fixture
@allure.description('Авторизация пользователя')
def auth_user(create_user):
    user_data = create_user['user_data']
    token = create_user['token']
    response = requests.post(f'{Config.URL}api/auth/login', headers={'Authorization': f'{token}'},
                             json={"email": user_data['email'], "password": user_data['password']})
    r = response.json()
    assert response.status_code == 200, f'Ожидается статус: 200, получен статус: {response.status_code}'
    token = r.get('accessToken')
    yield {'user_data': user_data, 'token': token}

@pytest.fixture
@allure.description('Создание заказа')
def create_order_auth_user(auth_user):
    user_data = auth_user['user_data']
    token = auth_user['token']
    data = {
        "ingredients": "61c0c5a71d1f82001bdaaa6d"
    }
    response = requests.post(f'{Config.URL}api/orders', headers={'Authorization': f'{token}'}, json=data)
    r = response.json()
    assert response.status_code == 200, \
        f'Ожидается статус: 200, получен статус: {response.status_code}'
    token = r.get('accessToken')
    yield {'user_data': user_data, 'token': token}

