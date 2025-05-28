import json
from queuemanager import QueueManager

class Hospital:
    def __init__(self, name, max_capacity,address, specialties=None):
        self.name = name
        self.max_capacity = max_capacity
        self.current_patients = 0
        self.specialties = specialties or []
        self.queue_manager = QueueManager()
        self.patient_queue = {
            'vermelho': [],
            'amarelo': [],
            'verde': []
        }
        self.address = address

    def can_accept_patient(self, priority):
        if priority == 'vermelho':
            return 'trauma' in self.specialties and self.current_patients < self.max_capacity
        elif priority == 'amarelo':
            return self.current_patients < self.max_capacity
        else:
            return self.current_patients < self.max_capacity

    def add_patient(self, patient_data):
        priority = patient_data.get('priority', 'verde')
        if self.can_accept_patient(priority):
            self.patient_queue[priority].append(patient_data)
            self.current_patients += 1
            return True
        return False

    def remove_patient(self, priority):
        if self.patient_queue[priority]:
            self.patient_queue[priority].pop(0)
            self.current_patients -= 1
            return True
        return False

    def callback(self, ch, method, properties, body):
        try:
            patient_data = json.loads(body.decode())
            print(f" [x] Received from {method.routing_key}: {patient_data}")

            if self.add_patient(patient_data):
                print(
                    f"Hospital {self.name} accepted patient. Current capacity: {self.current_patients}/{self.max_capacity}")
                ch.basic_ack(delivery_tag=method.delivery_tag)

                if properties.reply_to:
                    self.queue_manager.channel.basic_publish(
                        exchange='',
                        routing_key=properties.reply_to,
                        body=json.dumps({"address": self.address})
                    )
            else:
                print(
                    f"Hospital {self.name} cannot accept patient. Current capacity: {self.current_patients}/{self.max_capacity}")
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
                self.queue_manager.channel.stop_consuming()
        except json.JSONDecodeError:
            print(f"Error decoding message: {body.decode()}")

    def start_consuming(self):
        for queue in ['vermelho', 'amarelo', 'verde']:
            self.queue_manager.channel.basic_consume(
                queue=queue,
                on_message_callback=self.callback,
                auto_ack=False
            )
        print(f'Hospital {self.name} started consuming messages. To exit press CTRL+C')
        try:
            self.queue_manager.channel.start_consuming()
        except KeyboardInterrupt:
            print('Stopping...')
        finally:
            self.queue_manager.close()

if __name__ == '__main__':
    hospital = Hospital(
        name="Hospital Central",
        max_capacity=100,
        specialties=['trauma', 'emergency']
    )
    hospital.start_consuming()