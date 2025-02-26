from bababel.rabbitmq.rabbitmq_client import RabbitMQClient
from bababel.utils.utils import dict_to_bytes


class Publisher:
    def __init__(self, app):
        self.client = RabbitMQClient()
        self.connection = self.client.connect(host=app.host,
                                              port=app.port,
                                              username=app.username,
                                              password=app.password)
        self.app = app
        self.exchange()

    def publish(self, task_name: str, body: dict):
        self.connection.publish(exchange=self.app.identifier,
                                routing_key=task_name,
                                body=dict_to_bytes(body))

    def exchange(self):
        self.connection.declare_exchange(exchange=self.app.identifier)
