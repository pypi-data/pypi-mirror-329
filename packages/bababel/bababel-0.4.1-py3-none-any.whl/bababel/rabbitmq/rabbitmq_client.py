from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials

from bababel.rabbitmq.rabbitmq_connection import RabbitMQConnection


class RabbitMQClient:
    """
    Class responsible for communication with RabbitQ broker.
    """

    def connect(self, host: str, port: int, username: str, password: str) -> RabbitMQConnection:
        """
        Establishes a connection to a RabbitMQ broker.

        Args:
            host (str): The RabbitMQ server hostname or IP address.
            port (int): The port number for the RabbitMQ service.
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            RabbitMQConnection: An instance of RabbitMQConnection with the established connection.
        """
        credentials = PlainCredentials(username=username, password=password)

        params = ConnectionParameters(host=host, port=port, credentials=credentials)

        return RabbitMQConnection(parameters=params)
