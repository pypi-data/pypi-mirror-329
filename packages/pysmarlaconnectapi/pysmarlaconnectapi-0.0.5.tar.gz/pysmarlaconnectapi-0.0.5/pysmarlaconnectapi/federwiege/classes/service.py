from ...connection_hub import ConnectionHub
from .property import Property


class Service:
    props: list[Property] = []

    def __init__(self, connection_hub: ConnectionHub):
        self.hub = connection_hub
        self.registered = False

    def add_property(self, prop: Property):
        self.props.append(prop)

    def get_properties(self):
        return self.props

    def register(self):
        for prop in self.props:
            prop.register()
        self.registered = True

    def sync(self):
        for prop in self.props:
            prop.pull()
