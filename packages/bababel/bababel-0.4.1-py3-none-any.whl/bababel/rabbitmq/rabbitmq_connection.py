from pika.adapters.blocking_connection import (BlockingChannel,
                                               BlockingConnection)
from pika.connection import ConnectionParameters
from pika.spec import BasicProperties


class RabbitMQConnection:
    """
    RabbitMQConnection is a wrapper around pika's BlockingConnection to manage RabbitMQ communication.

    This class simplifies queue declaration and message consumption.

    Attributes:
        conn (BlockingConnection): The established RabbitMQ connection.
        channel (BlockingChannel): The communication channel for RabbitMQ operations.
    """

    def __init__(self, parameters: ConnectionParameters):
        """
        Initializes the RabbitMQ connection.

        Args:
            parameters (ConnectionParameters): The connection parameters required to establish the RabbitMQ connection.
        """
        self.conn: BlockingConnection = BlockingConnection(parameters=parameters)
        self.channel: BlockingChannel = self.conn.channel()

    def queue_declare(self, *args, **kwargs):
        """
        Declares a queue in RabbitMQ.

        Args:
            *args: Positional arguments for `pika.BlockingChannel.queue_declare`.
            **kwargs: Keyword arguments for `pika.BlockingChannel.queue_declare`.
        """
        return self.channel.queue_declare(*args, **kwargs)

    def basic_consume(self, *args, **kwargs):
        """
        Consumes messages from a queue.

        Args:
            *args: Positional arguments for `pika.BlockingChannel.basic_consume`.
            **kwargs: Keyword arguments for `pika.BlockingChannel.basic_consume`.
        """
        return self.channel.basic_consume(*args, **kwargs)

    def start_consuming(self):
        """
        Starts consuming messages from the queue.
        This method enters an infinite loop, listening for messages.
        """
        return self.channel.start_consuming()

    def process_events(self):
        return self.conn.process_data_events()

    def publish(self, exchange: str, routing_key: str, body: str | bytes, properties: BasicProperties = None):
        return self.channel.basic_publish(exchange=exchange,
                                          routing_key=routing_key,
                                          body=body,
                                          properties=properties)

    def declare_exchange(self, exchange: str):
        self.channel.exchange_declare(exchange=exchange)
