import pytest
import requests
from src.config import Config
import allure
from src.data import TextAnswers

class TestLoginUser:
    @allure.title('Проверка авторизации пользователя')
    @allure.description('Тест проверяет, что пользователь может авторизоваться')
    def test_login_user(self, create_user):
        user_data = create_user['user_data']
        user_data.pop('name')
        response = requests.post(f'{Config.URL}api/auth/login', json=user_data)
        assert response.status_code == 200, f'Ожидается статус: 200, получен статус: {response.status_code}'
        assert TextAnswers._textAuthorized200 in response.text, f'Ожидается текст ответа: "success":true , получен текст: {response.text}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка авторизации пользователя без логина или пароля, а так же с неправильными данными')
    @allure.description('Тест проверяет, что нельзя авторизоваться без логина или пароля, а так же с неверными логином или паролем')
    @pytest.mark.parametrize('email, password', [
        ('', 'password'),
        ('email', ''),
        ('email@', '12345678'),
        ('email@yandex.ru', '1')
    ])
    def test_login_user_without_data(self, create_user, email, password):
        user_data = create_user['user_data']
        user_data['email'] = email
        user_data['password'] = password
        user_data.pop('name')
        response = requests.post(f'{Config.URL}api/auth/login', json=user_data)
        r = response.json()
        assert response.status_code == 401, f'Ожидается статус: 401, получен статус: {response.status_code}'
        assert r["message"] == TextAnswers._textAuthorized401, \
            f'Ожидается текст ответа: Недостаточно данных для входа, получен текст: {r["message"]}'
        print(f' {response.status_code} {response.reason}. {r["message"]}')