import json
import uuid
import pika
from queuemanager import QueueManager


class Ambulancia:

    def __init__(self):
        # Create a unique reply queue for receiving messages
        self.reply_queue = f'resposta_ambulancia_{uuid.uuid4()}'
        self.queue_manager = QueueManager(queue_name=None)
        self.queue_manager.channel.queue_declare(queue=self.reply_queue)

    def send_message(self, priority, name, condition):
        message = json.dumps({
            'priority': priority,
            'name': name,
            'condition': condition
        })
        properties = pika.BasicProperties(reply_to=self.reply_queue)

        self.queue_manager.channel.basic_publish(
            exchange='',
            routing_key=priority,
            body=message,
            properties=properties
        )
        print(f" [x] Sent {message}")

    def receive_message(self):
        # Set up a consumer for the reply queue
        def callback(ch, method, properties, body):
            try:
                response = json.loads(body.decode())
                address = response.get("address", "No address provided")
                print(f" [x] Received hospital address: {address}")
            except json.JSONDecodeError:
                print(f"Error decoding message: {body.decode()}")
            finally:
                # Stop consuming after receiving one message
                self.queue_manager.channel.stop_consuming()

        self.queue_manager.channel.basic_consume(
            queue=self.reply_queue,
            on_message_callback=callback,
            auto_ack=True
        )

        # Start consuming messages (will stop after one message)
        print(f" [*] Waiting for one message on {self.reply_queue}.")
        self.queue_manager.channel.start_consuming()

    def run(self):
        print("Entrada: prioridade;nome;observação")
        print("digite 'exit' para sair.")

        while True:
            line = input('> ')
            if line.lower() == 'exit':
                break
            parts = [p.strip() for p in line.split(';')]

            if len(parts) != 3:
                print("Formato inválido.")
                continue

            # Send the message
            self.send_message(*parts)

            # Receive one message
            self.receive_message()


if __name__ == '__main__':
    ambulancia = Ambulancia()
    ambulancia.run()