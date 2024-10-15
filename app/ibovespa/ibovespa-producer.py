import time
import requests
from confluent_kafka import Producer
import json
import logging as log
from os import environ as env

# Function to send message to Kafka
def send_to_kafka(topic, message):
    producer.produce(topic, value=json.dumps(message))
    producer.flush()
    log.info(f"Message sent to Kafka")


kafka_server = env.get('KAFKA_SERVER', 'kafka1:9092')
interval = int(env.get('INTERVAL', 1))
log.basicConfig(level=log.INFO)

# Fetch JSON data from URL

# Kafka configuration
conf = {
    'bootstrap.servers': kafka_server,
    'client.id': 'ibovespa-producer'
}

# Create Producer instance
producer = Producer(conf)


while True:

    response = requests.get('https://b3api.me/api/quote/result')
    data = response.json()
    send_to_kafka('ibovespa_topic', data)
    time.sleep(2)
