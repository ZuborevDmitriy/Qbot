import json
from kafka import KafkaProducer

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

def send_in_kafka0(dummy_message):
    producer.send('messages0', dummy_message)

def send_in_kafka1(dummy_message):
    producer.send('messages1', dummy_message)
    
def upd_with_kafka(dummy_message):
    producer.send('updmess', dummy_message)