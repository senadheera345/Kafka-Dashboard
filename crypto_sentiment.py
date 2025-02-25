from kafka import KafkaProducer
import requests
import json
from textblob import TextBlob
import time

# NewsAPI Key (Replace this with your actual API key)
NEWS_API_KEY = "d91003dd08d04dfc9965c48933e48435"

# Set up Kafka Producer for Sentiment Analysis
sentiment_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define Sentiment Analysis Function
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

# Function to Fetch Crypto News and Send to Kafka
def fetch_crypto_news():
    url = f"https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()

    if "articles" in response:
        for article in response["articles"]:
            title = article["title"]
            sentiment = get_sentiment(title)
            data = {
                "title": title,
                "sentiment": sentiment,
                "source": article["source"]["name"],
                "url": article["url"]
            }
            print("Sending Sentiment Data:", data)
            sentiment_producer.send('crypto_sentiment', value=data)
    else:
        print("Error fetching news:", response)

# Run the sentiment producer every 10 seconds
while True:
    fetch_crypto_news()
    time.sleep(10)  # Fetch data every 10 seconds
