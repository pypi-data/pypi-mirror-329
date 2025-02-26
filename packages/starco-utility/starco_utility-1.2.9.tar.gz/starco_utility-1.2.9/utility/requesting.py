import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import aiohttp
import asyncio

# SyncRetryClient for synchronous requests


class SyncRetryClient:
    def __init__(self, retries=3, backoff_factor=1, status_forcelist=None, default_timeout=30):
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist or [429, 500, 502, 503, 504]
        self.default_timeout = default_timeout
        self.session = self._create_session()
    def _create_session(self):
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    
    def get(self, url, timeout=None, **kwargs):
        return self.session.get(url, timeout=timeout or self.default_timeout, **kwargs)

    def post(self, url, data=None, json=None, timeout=None, **kwargs):
        return self.session.post(url, data=data, json=json, timeout=timeout or self.default_timeout, **kwargs)

    def put(self, url, data=None, timeout=None, **kwargs):
        return self.session.put(url, data=data, timeout=timeout or self.default_timeout, **kwargs)

    def patch(self, url, data=None, timeout=None, **kwargs):
        return self.session.patch(url, data=data, timeout=timeout or self.default_timeout, **kwargs)

    def delete(self, url, timeout=None, **kwargs):
        return self.session.delete(url, timeout=timeout or self.default_timeout, **kwargs)


# AsyncRetryClient for asynchronous requests
class AsyncRetryClient:
    def __init__(self, retries=3, delay=2, status_forcelist=None,default_timeout=5):
        self.retries = retries
        self.delay = delay
        self.status_forcelist = status_forcelist or [429, 500, 502, 503, 504]
        self.default_timeout = default_timeout

    async def _fetch(self, session, url, method="GET", timeout=None, **kwargs):
        timeout = aiohttp.ClientTimeout(total=timeout or self.default_timeout)
        for attempt in range(1, self.retries + 1):
            try:
                if method.upper() == "GET":
                    async with session.get(url, timeout=timeout, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "POST":
                    async with session.post(url, timeout=timeout, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "PUT":
                    async with session.put(url, timeout=timeout, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "DELETE":
                    async with session.delete(url, timeout=timeout, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "PATCH":
                    async with session.patch(url, timeout=timeout, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
            except aiohttp.ClientError as e:
                print(f"Attempt {attempt}: Error - {e}")

            if attempt < self.retries:
                await asyncio.sleep(self.delay)

        raise Exception("All retry attempts failed")

    async def get(self, url, timeout=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="GET", timeout=timeout, **kwargs)

    async def post(self, url, data=None, json=None, timeout=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="POST", data=data, json=json, timeout=timeout, **kwargs)

    async def put(self, url, data=None, timeout=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="PUT", data=data, timeout=timeout, **kwargs)

    async def delete(self, url, timeout=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="DELETE", timeout=timeout, **kwargs)

    async def patch(self, url, timeout=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="PATCH", timeout=timeout, **kwargs)
