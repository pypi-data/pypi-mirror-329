import asyncio
import atexit

import aiohttp

DEFAULT_ENDPOINT_PROD = 'https://api.pushy.tg'


class PushyAPI:
    class Error(Exception):
        pass

    _endpoint: str
    _session: aiohttp.ClientSession

    def __init__(self, endpoint=DEFAULT_ENDPOINT_PROD):
        self._endpoint = endpoint
        self._session = aiohttp.ClientSession()

    @staticmethod
    async def create(endpoint=DEFAULT_ENDPOINT_PROD):
        api = PushyAPI(endpoint)
        await api.__aenter__()
        atexit.register(lambda: asyncio.run(api.__aexit__(None, None, None)))
        return api

    async def __aenter__(self):
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def do_request(self, method, path, params=..., body=None) -> dict:
        if params is ...:
            params = {}
        params = {k: self.__stringify_value(v) for k, v in params.items() if v is not None}
        async with self._session.request(method, self._endpoint + path, params=params, data=body) as response:
            if 200 <= response.status <= 299:
                return await response.json()
            if 500 <= response.status <= 599:
                raise self.Error(f"Internal Pushy API error: {response.status=}")
            if 400 <= response.status <= 499:
                details = ''
                try:
                    details = str(await response.json())
                except aiohttp.ContentTypeError:
                    pass
                raise self.Error(f'Bad request: {response.status=}, {details=}')

    async def get(self, path, params=..., body=None) -> dict:
        return await self.do_request('GET', path, params, body)

    async def post(self, path, params=..., body=None) -> dict:
        return await self.do_request('POST', path, params, body)

    async def put(self, path, params=..., body=None) -> dict:
        return await self.do_request('PUT', path, params, body)

    async def delete(self, path, params=..., body=None) -> dict:
        return await self.do_request('DELETE', path, params, body)

    @staticmethod
    def __stringify_value(value: bool | str | int | float):
        if isinstance(value, bool):
            return str(value).lower()
        return str(value)
