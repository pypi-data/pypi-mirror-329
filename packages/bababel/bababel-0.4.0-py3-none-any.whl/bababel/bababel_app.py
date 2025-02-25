import nanoid

from bababel.publisher.publisher import Publisher


class BababelApp:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.identifier = nanoid.generate()  # Exchange name for rabbitmq implementation
        self.publisher = Publisher(self)
