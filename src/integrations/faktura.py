import logging

import requests
from django.conf import settings
from django.core.cache import cache


logger = logging.getLogger(__name__)


class FakturaClient:
    """Документация: https://api.faktura.uz/docs/"""
    API_URL = settings.FAKTURA_API_URL
    AUTH_URL = settings.FAKTURA_AUTH_URL
    TOKEN_CACHE_KEY = "faktura-token"

    def get_token(self):
        """Получаем токен из кэша или запрашиваем новый."""
        token = cache.get(self.TOKEN_CACHE_KEY)
        if token:
            logger.info(f"Используем токен из Redis: {self.TOKEN_CACHE_KEY}")
            return token
        logger.info(f"Токен отсутствует в Redis. Запрашиваем новый: {self.TOKEN_CACHE_KEY}")
        data = {
            "grant_type": "password",
            "username": settings.FAKTURA_USERNAME,
            "password": settings.FAKTURA_PASSWORD,
            "client_id": settings.FAKTURA_CLIENT_ID,
            "client_secret": settings.FAKTURA_CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(f"{self.AUTH_URL}/token", data=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            cache.set(
                self.TOKEN_CACHE_KEY,
                response_json["access_token"],
                timeout=response_json["expires_in"] - 60  # Отнимаем 60 секунд во избежение проблем.
            )
            return response_json["access_token"]
        else:
            raise Exception(f"Ошибка получения токена: {response.text}")

    def make_request(self, method: str, endpoint: str, data=None, params=None):
        """Отправляет запрос с авторизацией."""
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Accept": "application/json",
        }
        url = f"{self.API_URL}{endpoint}"

        response = requests.request(method, url, headers=headers, json=data, params=params)
        return response.json()

    def get_company_basic_details(self, company_inn: str):
        params = {"companyInn": company_inn}
        """Получение информации об организации с указанным ИНН"""
        return self.make_request("GET", f"/Api/Company/GetCompanyBasicDetails", params=params)
