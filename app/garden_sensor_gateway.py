import time
import json
import random
import logging as  log
from os import environ as env
from confluent_kafka import Producer

previous_temp = 20.0
previous_humidity = 50.0
previous_wind = 5.0
previous_soil = 50.0

def random_temp_cels():
    global previous_temp
    # Add a small variation to the previous value
    variation = random.uniform(-2, 2)  # Variation from -2 to +2 degrees
    previous_temp = max(-10, min(50, previous_temp + variation))  # Ensure the value is within the range
    return round(previous_temp, 1)

def random_humidity():
    global previous_humidity
    variation = random.uniform(-5, 5)  # Variation from -5 to +5%
    previous_humidity = max(0, min(100, previous_humidity + variation))  # Ensure the value is within the range
    return round(previous_humidity, 1)

def random_wind():
    global previous_wind
    variation = random.uniform(-1, 1)  # Variation from -1 to +1
    previous_wind = max(0, min(10, previous_wind + variation))  # Ensure the value is within the range
    return round(previous_wind, 1)

def random_soil():
    global previous_soil
    variation = random.uniform(-5, 5)  # Variation from -5 to +5%
    previous_soil = max(0, min(100, previous_soil + variation))  # Ensure the value is within the range
    return round(previous_soil, 1)

def get_json_data():
    data = {}

    data["temperature"] = random_temp_cels()
    data["humidity"] = random_humidity()
    data["wind"] = random_wind()
    data["soil"] = random_soil()

    return json.dumps(data) 


def main():

    kafka_server = env.get('KAFKA_SERVER', 'kafka1:9092')
    buffer_size = int(env.get('BUFFER_SIZE', 20))
    interval = int(env.get('INTERVAL', 2))


    log.basicConfig(level=log.INFO)

    conf = {
        'bootstrap.servers': kafka_server,
        'client.id': 'garden_sensor_gateway'
    }
 

    producer = Producer(conf)

    while True:
        
        for _ in range(buffer_size):
            json_data = get_json_data()
            producer.produce('garden_sensor_data', bytes(f'{json_data}','UTF-8'))
            log.info(f"Sensor data is sent: {json_data}")
            time.sleep(interval)

        producer.flush()
        

   

if __name__ == "__main__":
    main()
