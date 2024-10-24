import pytest
import requests
from src.data import TextAnswers
from src.config import Config, TestData
import allure

class TestChangeUser:
    @allure.title('Проверка изменения данных пользователя')
    @allure.description('Тест проверяет, что можно изменить email и имя пользователя')
    @pytest.mark.parametrize('update_user_data', [
        ({'email': TestData.email}),
        ({'name': TestData.name})
    ])
    def test_change_auth_user(self, create_user, update_user_data):
        user_data = create_user['user_data']
        token = create_user['token']
        user_data.pop('password')
        response = requests.patch(f'{Config.URL}api/auth/user', headers={'Authorization': f'{token}'}, json=update_user_data)
        assert response.status_code == 200, f'Ожидается статус: 200, получен статус: {response.status_code}'
        assert TextAnswers._textChangeData200 in response.text, f'Ожидается текст ответа: "success":true , получен текст: {response.text}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка изменения почты пользователя с уже имеющейся почтой')
    @allure.description('Тест проверяет, что нельзя изменить почту пользователя, если таковая уже существует')
    def test_change_auth_user_with_existing_email(self, create_user):
        user_data = create_user['user_data']
        token = create_user['token']
        user_data.pop('password')
        update_user_data = {
            'email': TestData.email
        }
        response = requests.patch(f'{Config.URL}api/auth/user', headers={'Authorization': f'{token}'}, json=update_user_data)
        assert response.status_code == 403, f'Ожидается статус: 403, получен статус: {response.status_code}'
        assert TextAnswers._textChangeData403 in response.text, f'Ожидается текст ответа: "User with such email already exists" , получен текст: {response.text}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка изменения данных польpователя без авторизации')
    @allure.description('Тест проверяет, что нельзя изменить данные пользователя, если не авторизоваться')
    def test_change_auth_user_with_existing_email(self):
        update_user_data = {
            'email': TestData.email,
            'name': TestData.name
        }
        response = requests.patch(f'{Config.URL}api/auth/user', json=update_user_data)
        assert response.status_code == 401, f'Ожидается статус: 401, получен статус: {response.status_code}'
        assert TextAnswers._textChangeData401 in response.text, f'Ожидается текст ответа: "You should be authorised" , получен текст: {response.text}'
        print(f' {response.status_code} {response.reason}. {response.text}')

