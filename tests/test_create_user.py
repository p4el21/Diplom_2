import pytest
import requests
from src.data import TextAnswers
from src.helpers import generate_random_user
from src.config import Config
import allure

class TestCreateUser:
    @allure.title('Проверка создания пользователя')
    @allure.description('Тест проверяет, что можно создать пользователя')
    def test_create_new_user(self):
        user_data = generate_random_user()
        response = requests.post(f'{Config.URL}api/auth/register', json=user_data)
        assert response.status_code == 200, f'Ожидается статус: 200, получен статус: {response.status_code}'
        assert TextAnswers._textCreateUser200 in response.text, f'Ожидается текст ответа: "success":true , получен текст: {response.text}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка создания пользователя, который уже зарегистрирован')
    @allure.description('Тест проверяет, что нельзя создать пользователя,если email уже есть в системе')
    def test_create_new_user_with_existing_data(self):
        user_data = {
            "email": "p4el@yandex.ru",
            "password": "12345678",
            "name": "P4el11w11"
        }
        response = requests.post(f'{Config.URL}api/auth/register', json=user_data)
        r = response.json()
        assert response.status_code == 403, f'Ожидается статус: 403, получен статус: {response.status_code}'
        assert TextAnswers._textCreateExistingUser403 in r['message'], \
            f'Ожидается текст ответа: Этот логин уже используется, получен текст: {r["message"]}'
        print(f' {response.status_code} {response.reason}. {r["message"]}')

    @allure.title('Проверка создания пользователя без одного из обязательных полей')
    @allure.description('Тест проверяет, что нельзя создать пользователя без почты, имени или пароля')
    @pytest.mark.parametrize('email, password, name', [('', 'password', 'name',),('email', '', 'name'),('email', 'password', '')])
    def test_create_courier_without_login(self, email, password, name):
        user_data = generate_random_user()
        user_data = {
            user_data['email']: "email",
            user_data['password']: "password",
            user_data['name']: "name"
        }
        response = requests.post(f'{Config.URL}api/auth/register', json=user_data)
        r = response.json()
        assert response.status_code == 403, f'Ожидается статус: 403, получен статус: {response.status_code}'
        assert r['message'] == TextAnswers._textCreateUserWithoutField403,\
            f'Ожидается текст ответа: Email, password and name are required fields, получен текст: {r["message"]}'
        print(f' {response.status_code} {response.reason}. {r["message"]}')