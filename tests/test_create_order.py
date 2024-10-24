import pytest
import requests
from src.data import TextAnswers
from src.config import Config
import allure

class TestCreateOrder:
    @allure.title('Проверка создания заказа с ингредиентами после авторизации пользователя')
    @allure.description('Тест проверяет, что авторизованный пользователь может создать заказ, добавив ингредиент')
    def test_create_order_auth_user(self, auth_user):
        token = auth_user['token']
        data = {
            "ingredients": "61c0c5a71d1f82001bdaaa6d"
        }
        response = requests.post(f'{Config.URL}api/orders', headers={'Authorization': f'{token}'}, json=data)
        r = response.json()
        assert response.status_code == 200, \
            f'Ожидается статус: 200, получен статус: {response.status_code}'
        assert r['success'] == True, f'Ожидается ответ: True, получен {r['success']}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка создания заказа с ингредиентами неавторизованным пользователем')
    @allure.description('Тест проверяет, что неавторизованный пользователь может создать заказ, добавив ингредиент')
    def test_create_order(self):
        user_data = {
            "ingredients": "61c0c5a71d1f82001bdaaa6d"
        }
        response = requests.post(f'{Config.URL}api/orders', json=user_data)
        r = response.json()
        assert response.status_code == 200, \
            f'Ожидается статус: 200, получен статус: {response.status_code}'
        assert r['success'] == True, f'Ожидается ответ: True, получен {r['success']}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка создания заказа без ингредиентов после авторизации пользователя')
    @allure.description('Тест проверяет, что авторизованный пользователь не может создать заказ,не добавив ингредиенты')
    def test_create_order_auth_user_without_ingredients(self, auth_user):
        token = auth_user['token']
        user_data = {}
        response = requests.post(f'{Config.URL}api/orders', headers={'Authorization': f'{token}'}, json=user_data)
        r = response.json()
        assert response.status_code == 400, f'Ожидается статус: 400, получен статус: {response.status_code}'
        assert r['message'] == TextAnswers._textCreateOrder400, \
            f'Ожидется текст: "Ingredient ids must be provided", получен текст: {r["message"]}'
        assert r['success'] == False, \
            f'Ожидется текст: "False", получен текст: {r["success"]}'
        print(f' {response.status_code} {response.reason}. {r['message']}')

    @allure.title('Проверка создания заказа без авторизации и ингредиентов')
    @allure.description('Тест проверяет, что нельзя создать заказ, не добавляя ингредиенты')
    def test_create_order_without_ingredients(self):
        response = requests.post(f'{Config.URL}api/orders')
        r = response.json()
        assert response.status_code == 400, f'Ожидается статус: 400, получен статус: {response.status_code}'
        assert r['message'] == TextAnswers._textCreateOrder400, \
            f'Ожидется текст: "Ingredient ids must be provided", получен текст: {r["message"]}'
        assert r['success'] == False, \
            f'Ожидется текст: "False", получен текст: {r["success"]}'
        print(f' {response.status_code} {response.reason}. {r['message']}')

    @allure.title('Проверка создания заказа c невалидным хешем ингредиента')
    @allure.description('Тест проверяет, что нельзя создать заказ, вводя невалидный хеш ингредиента')
    def test_create_order_invalid_hash(self):
        user_data = {
            "ingredients": "61c0c5fdsa71d1f82001bdaaa6d"
        }
        response = requests.post(f'{Config.URL}api/orders', json=user_data)
        assert response.status_code == 500, \
            f'Ожидается статус: 500, получен статус: {response.status_code}'
        print(f' {response.status_code} {response.reason}. {response.text}')



