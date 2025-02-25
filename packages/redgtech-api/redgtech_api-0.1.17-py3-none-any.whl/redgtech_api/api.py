import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

API_URL = "https://redgtech-dev.com"

class RedgtechAPI:
    def __init__(self, token=None):
        self._token = token

    async def login(self, email, password):
        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/home_assistant/login"
            async with session.post(url, json={'email': email, 'password': password}) as response:
                response.raise_for_status()
                data = await response.json()
                self._token = data.get('data', {}).get('access_token')
                return self._token

    async def get_data(self, token=None):
        token = token or self._token
        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/home_assistant?access_token={token}"
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
              

    async def set_switch_state(self, endpoint_id, state, token=None):
        token = token or self._token
        id_part, after_id = endpoint_id.split("-", 1)
        number_channel = after_id[-1]
        type_channel = ''.join(char for char in after_id if char.isalpha())
        state_char = 'l' if state else 'd'
        value = f"{number_channel}{state_char}" if type_channel == "AC" else f"{type_channel}{number_channel}*{state_char}*"
        url = f"{API_URL}/home_assistant/execute/{id_part}?cod=?{value}"
        headers = {"Authorization": f"{token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return response.status == 200

    async def set_light_brightness(self, endpoint_id, brightness, token=None):
        token = token or self._token
        id_part, after_id = endpoint_id.split("-", 1)
        number_channel = after_id[-1]
        type_channel = ''.join(char for char in after_id if char.isalpha())
        brightness_value = round((brightness / 255) * 100)
        value = f"{type_channel}{number_channel}*{brightness_value}*"
        url = f"{API_URL}/home_assistant/execute/{id_part}?cod=?{value}"
        headers = {"Authorization": f"{token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return response.status == 200