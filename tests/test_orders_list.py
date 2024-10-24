import requests
from src.config import Config
import allure
from src.data import TextAnswers

class TestOrdersList:
    @allure.title('Проверка получения списка заказов авторизованного пользователя')
    @allure.description('Тест на получение списка заказов, если посльзователь авторизован')
    def test_get_orders_list_auth_user(self, create_order_auth_user, auth_user):
        token = auth_user['token']
        user_data = create_order_auth_user['user_data']
        response = requests.get(f'{Config.URL}api/orders', headers={'Authorization': f'{token}'}, json=user_data)
        assert response.status_code == 200, f'Ожидается статус: 200, получен статус: {response.status_code}'
        print(f' {response.status_code} {response.reason}. {response.text}')

    @allure.title('Проверка получения списка заказов неавторизованного пользователя')
    @allure.description('Тест на получение списка заказов, если пользователь не авторизован')
    def test_get_orders_list_unauth_user(self):
        response = requests.get(f'{Config.URL}api/orders')
        r = response.json()
        assert response.status_code == 401, f'Ожидается статус: 401, получен статус: {response.status_code}'
        assert r['message'] == TextAnswers._textOrdersList401, \
            f'Ожидется текст: "You should be authorised", получен текст: {r["message"]}'
        assert r['success'] == False, \
            f'Ожидется текст: "False", получен текст: {r["success"]}'
        print(f' {response.status_code} {response.reason}. {response.text}')