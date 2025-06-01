from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'avg_fare_per_hour',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='verify-consumer'
)

print("Listening for aggregated fare messages...")
for msg in consumer:
    print(msg.value)