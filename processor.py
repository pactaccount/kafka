import json
import statistics
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer(
    'nyc_taxi_trips',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='trip-processor'
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
output_topic = 'avg_fare_per_hour'

hourly_fares = {}
for msg in consumer:
    trip = msg.value
    pickup_dt = trip['tpep_pickup_datetime']
    hour = pickup_dt.split(' ')[1].split(':')[0]
    fare = float(trip.get('fare_amount', 0) or 0)

    hourly_fares.setdefault(hour, []).append(fare)
    if len(hourly_fares[hour]) >= 1000:
        avg_fare = statistics.mean(hourly_fares[hour])
        producer.send(output_topic, {'hour': hour, 'average_fare': avg_fare})
        hourly_fares[hour].clear()