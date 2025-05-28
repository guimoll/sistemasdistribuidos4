from hospital import Hospital

class UPA(Hospital):
    def __init__(self, name="UPA", max_capacity=30):
        super().__init__(
            name=name,
            max_capacity=max_capacity,
            specialties=['general', 'basic_care'],
            address="R. Norberto Seara Heusi, 477 - Escola Agrícola, Blumenau - SC, 89037-800"
        )

    def start_consuming(self):
        self.queue_manager.channel.basic_consume(
            queue='verde',
            on_message_callback=self.callback,
            auto_ack=False
        )
        print(f'{self.name} started consuming UPA (verde) messages. To exit press CTRL+C')
        try:
            self.queue_manager.channel.start_consuming()
        except KeyboardInterrupt:
            print('Stopping...')
        finally:
            self.queue_manager.close()

if __name__ == '__main__':
    upa = UPA()
    upa.start_consuming()