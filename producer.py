from kafka import KafkaProducer
import json
import requests
import time

# Set up Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Cryptos to track
crypto_pairs = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']

def fetch_crypto_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url).json()
    return {data['symbol']: data['price'] for data in response if data['symbol'] in crypto_pairs}

while True:
    prices = fetch_crypto_prices()
    print("Sending:", prices)
    producer.send('crypto_prices', value=prices)
    time.sleep(2)  # Fetch data every 2 seconds
