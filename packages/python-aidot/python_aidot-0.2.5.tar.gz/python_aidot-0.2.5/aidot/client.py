"""The aidot integration."""

import logging
from typing import Any, Optional
from aiohttp import ClientResponseError, ClientSession
import base64
import aiohttp
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .login_const import APP_ID, PUBLIC_KEY_PEM, BASE_URL
from .const import (
    SUPPORTED_COUNTRYS,
    DEFAULT_COUNTRY_NAME,
    CONF_PRODUCT_ID,
    CONF_ID,
    CONF_PRODUCT,
    CONF_ACCESS_TOKEN,
    CONF_REFRESH_TOKEN,
    CONF_TERMINAL,
    CONF_APP_ID,
)
from .exceptions import AidotAuthFailed

_LOGGER = logging.getLogger(__name__)


def rsa_password_encrypt(message: str):
    """Get password rsa encrypt."""
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY_PEM, backend=default_backend()
    )

    encrypted = public_key.encrypt(
        message.encode("utf-8"),
        padding.PKCS1v15(),
    )

    encrypted_base64 = base64.b64encode(encrypted).decode("utf-8")
    return encrypted_base64


class AidotClient:
    _base_url: str = BASE_URL
    _region: str = "us"
    session: Optional[ClientSession] = None
    username: str = ""
    password: str = ""
    country_name: str = DEFAULT_COUNTRY_NAME
    login_info: dict[str, Any] = {}

    def __init__(
        self,
        country_name: str | None = None,
        username: str | None = None,
        password: str | None = None,
        token: dict | None = None,
    ) -> None:
        self.country_name = country_name
        self.username = username
        self.password = password
        self.login_info = token
        for item in SUPPORTED_COUNTRYS:
            if item["name"] == self.country_name:
                self._region = item["region"].lower()
                self._base_url = f"https://prod-{self._region}-api.arnoo.com/v17"
                break

    def get_identifier(self) -> str:
        return f"{self.username}-{self.password}-{self._region}"

    async def async_post_login(self):
        """Login the user input allows us to connect."""
        url = f"{self._base_url}/users/loginWithFreeVerification"
        headers = {CONF_APP_ID: APP_ID, CONF_TERMINAL: "app"}
        data = {
            "countryKey": "region:UnitedStates",
            "username": self.username,
            "password": rsa_password_encrypt(self.password),
            "terminalId": "gvz3gjae10l4zii00t7y0",
            "webVersion": "0.5.0",
            "area": "Asia/Shanghai",
            "UTC": "UTC+8",
        }

        try:
            async with self.session.post(url, headers=headers, json=data) as response:
                response.raise_for_status()
                self.login_info = await response.json()
                return self.login_info
        except aiohttp.ClientError as e:
            _LOGGER.info("async_post_login ClientError {e}")
            return None

    async def async_refresh_token(self):
        url = f"{self._base_url}/users/refreshToken"
        headers = {CONF_APP_ID: APP_ID, CONF_TERMINAL: "app"}
        data = {
            CONF_REFRESH_TOKEN: self.login_info[CONF_REFRESH_TOKEN],
        }

        try:
            async with self.session.post(url, headers=headers, json=data) as response:
                response.raise_for_status()
                data = await response.json()
                self.login_info[CONF_ACCESS_TOKEN] = data[CONF_ACCESS_TOKEN]
                return data
        except aiohttp.ClientError as e:
            _LOGGER.info("async_post_login ClientError {e}")
            return None

    async def async_session_get(self, params: str, headers: str | None = None):
        url = f"{self._base_url}{params}"
        token = self.login_info[CONF_ACCESS_TOKEN]
        if token is None:
            raise AidotAuthFailed()
        if headers is None:
            headers = {
                CONF_TERMINAL: "app",
                "Token": token,
                CONF_APP_ID: APP_ID,
            }
        try:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                response_data = await response.json()
                return response_data
        except aiohttp.ClientError as e:
            _LOGGER.info("async_get_products ClientError {e}")
            return None

    async def async_get_products(self, product_ids: str):
        """Get device list."""
        params = f"/products/{product_ids}"
        return await self.async_session_get(params)

    async def async_get_devices(self, house_id: str):
        """Get device list."""
        params = f"/devices?houseId={house_id}"
        return await self.async_session_get(params)

    async def async_get_houses(self, token: str):
        """Get house list."""
        params = "/houses"
        return await self.async_session_get(params)

    async def async_get_all_device(self):
        # get houses
        houses = await self.async_get_houses()
        final_device_list: list[dict[str, Any]] = []
        for house in houses:
            # get device_list
            device_list = await self.async_get_devices(house[CONF_ID])
            if device_list:
                final_device_list.extend(device_list)

        # get product_list
        productIds = ",".join([item[CONF_PRODUCT_ID] for item in device_list])
        product_list = await self.async_get_products(productIds)

        for product in product_list:
            for device in final_device_list:
                if device[CONF_PRODUCT_ID] == product[CONF_ID]:
                    device[CONF_PRODUCT] = product
        return final_device_list
