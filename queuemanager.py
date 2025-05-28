import ssl

import pika


class QueueManager:
    _connections = []

    def __init__(self, queue_name='hello'):
        context = ssl.create_default_context(cafile='C:/Users/riley/PycharmProjects/PythonProject2/certs/ca.crt')
        context.load_cert_chain(
            certfile='C:/Users/riley/PycharmProjects/PythonProject2/certs/client.crt',
            keyfile='C:/Users/riley/PycharmProjects/PythonProject2/certs/client.key'
        )
        ssl_options = pika.SSLOptions(context, 'localhost')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5671,
                ssl_options=ssl_options
            )
        )
        self.channel = self.connection.channel()

        for q in ['vermelho', 'amarelo', 'verde']:
            self.channel.queue_declare(queue=q)
        QueueManager._connections.append(self.connection)

    def close(self):
        for conn in QueueManager._connections:
            if conn and not conn.is_closed:
                conn.close()
        QueueManager._connections.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    with QueueManager() as qm:
        print("QueueManager is running. Press Enter to close all connections.")
        input()
