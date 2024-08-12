import json

from confluent_kafka import Consumer, Producer

from broker.topics import Topics

#  TODO: assign from .env
producer_config = {
    "bootstrap.servers": "kafka:29092",
    'acks': 'all'
    # lambda x: json.dumps(x).encode('utf-8')
}

consumer_config = {
    "bootstrap.servers": "kafka:29092",
    'group.id': 'broker',
    'enable.auto.commit': True,
    'auto.commit.interval.ms': 1000,
}

generic_producer: Producer = Producer(**producer_config)


class KafkaMiddleware:
    service: str
    consumer: Consumer
    producer: Producer

    def __init__(self, service_name: str):
        consumer_config["group.id"] = service_name
        self.consumer: Consumer = Consumer(**consumer_config)
        self.producer = generic_producer

    def send_message(self, topic: Topics, message: dict):
        self.producer.produce(topic.value, value=json.dumps(message).encode('utf-8'))
        print(self.producer.flush())

    def get_message(self):
        return self.consumer.next()

    @staticmethod
    def get_consumer(client_id: str, group_id: str):
        consumer_config["group.id"] = group_id
        consumer_config["client.id"] = client_id
        return Consumer(**consumer_config)

    @staticmethod
    def get_producer(topic: Topics):
        producer_config["client.id"] = topic.value
        return generic_producer
