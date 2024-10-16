# Garden Sensor Gateway

Inspired by and forked from the [InfluxDB Community Kafka Demo](https://github.com/InfluxCommunity/influxdb-kafka-demo).

## Environment Variables

- `KAFKA_SERVER`: The Kafka bootstrap server address (default: `kafka1:9092`).

## Usage

To run the container, use the following command:

```sh
docker run -e KAFKA_SERVER=<your_kafka_server> garden_sensor_gateway
```

This will start the container and begin sending random sensor data to the garden_sensor_data Kafka topic.