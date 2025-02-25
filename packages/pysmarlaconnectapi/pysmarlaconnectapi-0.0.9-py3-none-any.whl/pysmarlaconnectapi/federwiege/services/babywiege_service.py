from ...connection_hub import ConnectionHub
from ..classes import Property, Service


class BabywiegeService(Service):

    def __init__(self, connection_hub: ConnectionHub):
        super().__init__(connection_hub)
        self.swing_active = SwingActiveProperty(self.hub)
        self.add_property(self.swing_active)
        self.register()


class SwingActiveProperty(Property[bool]):

    async def on_callback(self, args):
        value = args[0]["value"]
        self.set(value, push=False)
        async with self.lock:
            for listener in self.listeners:
                await listener(value)

    def __init__(self, parent: Service):
        super().__init__(parent)
        self.value = False

    def pull(self):
        self.hub.send_serialized_data("GetSwingActive")

    def push(self, value):
        self.hub.send_serialized_data("SetSwingActive", value)

    def register(self):
        self.hub.client.on("GetSwingActiveCallback", self.on_callback)
