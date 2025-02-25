A messaging consumer library for handling and processing messages efficiently.
It is meant to simplify message publishing and processing.

In the current ver version you can only send tasks to a exchange:

Example usage:

    from bababel.bababel_app import BababelApp
    from bababel.task.task import Task

    # Sample Bababel Task
    class SampleTask(Task):
        def run(self, xpto):
            return xpto

    # Declare the BababelApp
    app = BababelApp(host='localhost',
                     port=5672,
                     username='guest',
                     password='guest')

    # Declare the task
    task = SampleTask(app=app)

    # Send message to the consumer (to be implemented)
    # The consumer will execute task.run with the parameters given in the send method
    task.send(message='xpto', code=123)

This project uses conventional commits 1.0.0
