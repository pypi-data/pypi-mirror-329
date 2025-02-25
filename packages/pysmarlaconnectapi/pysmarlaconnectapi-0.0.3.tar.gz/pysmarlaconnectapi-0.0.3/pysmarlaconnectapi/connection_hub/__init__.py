import asyncio
import logging
import random
import uuid

import aiohttp
import jsonpickle
from pysignalr.client import SignalRClient
from pysignalr.transport.abstract import ConnectionState

from ..classes import AuthToken, ConnectionConfig

_logger = logging.getLogger("pysmarlaconnectapi.connectionhub")


async def event_wait(event, timeout):
    try:
        await asyncio.wait_for(event.wait(), timeout)
    except asyncio.TimeoutError:
        return


class ConnectionHub:
    """SignalRCore Hub
    Provides interface via websocket for the controller using the SignalRCore protocol.
    """

    config: ConnectionConfig
    _loop: asyncio.AbstractEventLoop

    @property
    def running(self):
        return self._running

    @property
    def connected(self):
        return self.client._transport._state == ConnectionState.connected if self.client else False

    def __init__(
        self, async_loop: asyncio.AbstractEventLoop, config: ConnectionConfig, interval: int = 60, backoff: int = 300
    ):
        self.config = config
        self._loop = async_loop
        self._interval = interval
        self._backoff = backoff

        self._running = False
        self._wake = asyncio.Event()

        self.client = None
        self.setup()

    def setup(self):
        self.client = SignalRClient(self.config.url + "/MobileAppHub", retry_count=1)
        self.client.on_open(self.on_open_function)
        self.client.on_close(self.on_close_function)
        self.client.on_error(self.on_error)

    async def on_open_function(self):
        _logger.info("Connection to server established")

    async def on_close_function(self):
        _logger.info("Connection to server closed")

    async def on_error(self, message):
        _logger.error("Connection error occurred: " + str(message))

    def start(self):
        if self.running:
            return
        self._running = True
        asyncio.run_coroutine_threadsafe(self.connection_watcher(), self._loop)

    def stop(self):
        if not self.running:
            return
        self._running = False
        self.close_connection()
        self.wake_up()

    async def connection_watcher(self):
        while self.running:
            try:
                await self.refresh_token()
                await self.client.run()
            except Exception as e:
                _logger.error(f"Error during connection: {type(e).__name__}: {str(e)}")

            # Random backoff to avoid simultaneous connection attempts
            backoff = random.randint(0, self._backoff)
            await event_wait(self._wake, self._interval + backoff)
            self._wake.clear()

    def wake_up(self):
        self._wake.set()

    def close_connection(self):
        if not self.connected:
            return
        asyncio.run_coroutine_threadsafe(self.client._transport._ws.close(), self._loop)

    async def refresh_token(self):
        auth_token = await self.get_token(self.config.token)
        self.config.token = auth_token
        self.client._transport._headers["Authorization"] = f"Bearer {self.config.token.token}"
        _logger.info("Auth token refreshed")

    async def get_token(self, refresh_token: AuthToken) -> AuthToken:
        async with aiohttp.ClientSession(self.config.url) as session:
            async with session.post(
                "/api/AppParing/getToken",
                headers={"accept": "*/*", "Content-Type": "application/json"},
                data=jsonpickle.encode(refresh_token, unpicklable=False),
            ) as response:
                if response.status == 200:
                    json_body = await response.json()
                    return AuthToken.from_json(json_body)

    def send_serialized_data(self, event, value=None):
        if not self.connected:
            return

        serialized_result = {
            "callIdentifier": {
                "requestNonce": str(uuid.uuid4()),
            },
        }
        if value is not None:
            serialized_result["value"] = value

        _logger.debug(f"Sending data, Event: {event}, Payload: {str(serialized_result)}")

        asyncio.run_coroutine_threadsafe(self.send_data(event, [serialized_result]), self._loop)

    async def send_data(self, event, data):
        try:
            await self.client.send(event, data)
        except Exception:
            pass
