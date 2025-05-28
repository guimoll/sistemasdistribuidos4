from hospital import Hospital

class HospitalMedio(Hospital):
    def __init__(self, name="Hospital Médio", max_capacity=100, address="R. Itajaí, 545 - Vorstadt, Blumenau - SC, 89015-200"):
        super().__init__(
            name=name,
            max_capacity=max_capacity,
            specialties=['emergency', 'general'],
            address = address
        )

    def start_consuming(self):
        self.queue_manager.channel.basic_consume(
            queue='amarelo',
            on_message_callback=self.callback,
            auto_ack=False
        )
        print(f'{self.name} started consuming medium (amarelo) messages. To exit press CTRL+C')
        try:
            self.queue_manager.channel.start_consuming()
        except KeyboardInterrupt:
            print('Stopping...')
        finally:
            self.queue_manager.close()

if __name__ == '__main__':
    medio_hospital = HospitalMedio()
    medio_hospital.start_consuming()