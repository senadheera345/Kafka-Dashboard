from kafka import KafkaConsumer
import json

# Set up Kafka Consumer for Both Topics
consumer = KafkaConsumer(
    'crypto_prices', 'crypto_sentiment',  # Subscribing to both topics
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Waiting for messages...")
for message in consumer:
    if message.topic == 'crypto_prices':
        print("📊 Price Update:", message.value)
    elif message.topic == 'crypto_sentiment':
        print("📰 Sentiment Update:", message.value)
