import time
import json
import random
from kafka import KafkaProducer

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

def send_in_kafka(dummy_message):
    producer.send('messages', dummy_message)