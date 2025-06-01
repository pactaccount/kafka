import csv
import time
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic = 'nyc_taxi_trips'

dataset_path = 'data/converted.csv'
with open(dataset_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        producer.send(topic, row)
        time.sleep(0.01)

producer.flush()
producer.close()