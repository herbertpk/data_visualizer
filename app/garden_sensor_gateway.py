import time
import json
import random
import logging as  log
from os import environ as env
from confluent_kafka import Producer
import math

previous_temp = 20.0
previous_humidity = 50.0
previous_wind = 5.0
previous_soil = 50.0

def set_variation_based_on_interval(interval):
    """Adjusts variation based on the interval using a logarithmic scale."""
    # Use a logarithmic scale to determine variation
    # Adding 1 to avoid log(0) which is undefined
    log_interval = math.log(interval + 1)
    # Scale the logarithmic value to the desired variation range
    variation = max(log_interval)
    return variation


def random_temp_cels(interval):
    global previous_temp
    variation = set_variation_based_on_interval(interval)
    change = random.uniform(-variation, variation)  # Use the adjusted variation
    previous_temp = max(-10, min(50, previous_temp + change))
    return round(previous_temp, 1)

def random_humidity(interval):
    global previous_humidity
    variation = set_variation_based_on_interval(interval)
    change = random.uniform(-variation, variation)
    previous_humidity = max(0, min(100, previous_humidity + change))
    return round(previous_humidity, 1)

def random_wind(interval):
    global previous_wind
    variation = set_variation_based_on_interval(interval)
    change = random.uniform(-variation, variation)
    previous_wind = max(0, min(10, previous_wind + change))
    return round(previous_wind, 1)

def random_soil(interval):
    global previous_soil
    variation = set_variation_based_on_interval(interval)
    change = random.uniform(-variation, variation)
    previous_soil = max(0, min(100, previous_soil + change))
    return round(previous_soil, 1)

def get_json_data(interval):
    data = {}

    data["temperature"] = random_temp_cels(interval)
    data["humidity"] = random_humidity(interval)
    data["wind"] = random_wind(interval)
    data["soil"] = random_soil(interval)

    return json.dumps(data) 


def main():

    kafka_server = env.get('KAFKA_SERVER', 'kafka1:9092')
    buffer_size = int(env.get('BUFFER_SIZE', 20))
    interval = int(env.get('INTERVAL', 1))


    log.basicConfig(level=log.INFO)

    conf = {
        'bootstrap.servers': kafka_server,
        'client.id': 'garden_sensor_gateway'
    }
 

    producer = Producer(conf)

    while True:
        
        for _ in range(buffer_size):
            json_data = get_json_data(interval)
            producer.produce('garden_sensor_data', bytes(f'{json_data}','UTF-8'))
            log.info(f"Sensor data is sent: {json_data}")
            time.sleep(interval)

        producer.flush()
        

   

if __name__ == "__main__":
    main()
