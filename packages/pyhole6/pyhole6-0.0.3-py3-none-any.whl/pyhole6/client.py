import aiohttp
from typing import Optional
from .logger import setup_logger
from .exceptions import AuthenticationError
from .models import Session


class Pyhole6:
    def __init__(self, base_url: str, password: str):
        self.base_url = f"{base_url}/api"
        self.password = password
        self.session: Optional[aiohttp.ClientSession] = None
        self.session_obj: Optional[Session] = None
        self.logger = setup_logger()
        self._authenticated = False

        # Resources
        self._history = None
        self._stats = None
        self._dns = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    @property
    def is_authenticated(self):
        return self._authenticated and self.session_obj is not None

    async def connect(self):
        self.session = aiohttp.ClientSession()
        await self.authenticate()
        if self._authenticated:

            from .resources.history import HistoryResource
            self._history = HistoryResource(self)

            from .resources.stats import StatsResource
            self._stats = StatsResource(self)

            from .resources.dns import DNSResource
            self._dns = DNSResource(self)

    async def disconnect(self):
        await self.logout()
        if self.session:
            await self.session.close()

    async def authenticate(self):
        self.logger.info(f"Authenticating with {self.base_url}")
        async with self.session.post(f"{self.base_url}/auth",
                                   json={"password": self.password}) as response:
            data = await response.json()
            if data.get("session", {}).get("valid"):
                self.session_obj = Session(**data.get('session'))
                self._authenticated = True
                self.logger.info("Authenticated")
            else:
                msg = f"Authentication failed. {data.get('session', {}).get('message')}"
                self.logger.error(msg)
                await self.session.close()
                raise AuthenticationError(msg)

    async def sessions(self):
        async with self.session.get(f"{self.base_url}/auth/sessions",
                                    headers={"sid": self.session_obj.sid}) as response:
            data = await response.json()
            if response.status == 200:
                return data
            else:
                await self.session.close()
                raise AuthenticationError(data.get('error'))

    async def logout(self):
        if self.session_obj.sid:
            await self.session.delete(f"{self.base_url}/auth", headers={"sid": self.session_obj.sid})

    @property
    def history(self):
        if not self._authenticated:
            raise RuntimeError("Client is not authenticated. Call connect() first.")
        return self._history

    @property
    def stats(self):
        if not self._authenticated:
            raise RuntimeError("Client is not authenticated. Call connect() first.")
        return self._stats

    @property
    def dns(self):
        if not self._authenticated:
            raise RuntimeError("Client is not authenticated. Call connect() first.")
        return self._dns