import asyncio
from typing import Generic, TypeVar

from ...connection_hub import ConnectionHub

_VT = TypeVar("_VT")


class Property(Generic[_VT]):
    value: _VT = None
    listeners = set()
    lock = asyncio.Lock()

    def __init__(self, connection_hub: ConnectionHub):
        self.hub = connection_hub

    async def add_listener(self, listener):
        async with self.lock:
            self.listeners.add(listener)

    async def remove_listener(self, listener):
        async with self.lock:
            self.listeners.remove(listener)

    def get(self) -> _VT:
        return self.value

    def set(self, new_value: _VT, push=True):
        if push:
            self.push(new_value)
        else:
            self.value = new_value

    def push(self):
        pass

    def pull(self):
        pass

    def register(self):
        pass
