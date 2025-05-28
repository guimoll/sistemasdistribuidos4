from hospital import Hospital

class HospitalTrauma(Hospital):
    def __init__(self, name="Hospital de Trauma", max_capacity=3):
        super().__init__(
            name=name,
            max_capacity=max_capacity,
            specialties=['trauma', 'emergency', 'surgery'],
            address="R. Floriano Peixoto, 300 - Centro, Blumenau - SC, 89010-906"
        )

    def start_consuming(self):
        self.queue_manager.channel.basic_consume(
            queue='vermelho',
            on_message_callback=self.callback,
            auto_ack=False
        )
        print(f'{self.name} started consuming trauma (vermelho) messages. To exit press CTRL+C')
        try:
            self.queue_manager.channel.start_consuming()
        except KeyboardInterrupt:
            print('Stopping...')
        finally:
            self.queue_manager.close()


if __name__ == '__main__':
    trauma_hospital = HospitalTrauma()
    trauma_hospital.start_consuming()
