import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
import plotly.express as px

# Set up Kafka Consumer for both prices & sentiment
consumer = KafkaConsumer(
    'crypto_prices', 'crypto_sentiment',  
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Streamlit Dashboard
st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("📊 Live Crypto Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a section", ["Home", "Live Crypto Prices", "Sentiment Analysis"])

# Create placeholders for prices & sentiment
price_placeholder = st.empty()
sentiment_placeholder = st.empty()

# Data containers
prices_df = pd.DataFrame(columns=["Crypto", "Price"])
sentiment_df = pd.DataFrame(columns=["Title", "Sentiment", "Source"])

# Real-time update loop
for message in consumer:
    if message.topic == "crypto_prices":
        prices = message.value
        prices_df = pd.DataFrame(prices.items(), columns=["Crypto", "Price"])
        
        # Ensure prices are numeric
        prices_df["Price"] = pd.to_numeric(prices_df["Price"], errors="coerce")
        
        # Home page content
        if page == "Home":
            st.markdown("""
            Welcome to the live crypto dashboard!  
            This dashboard provides real-time insights into cryptocurrency prices and market sentiment.  
            Use the navigation bar to explore live price data and sentiment analysis.
            """)

        # Update price table and chart in columns layout
        if page == "Live Crypto Prices":
            with price_placeholder.container():
                col1, col2 = st.columns([2, 3])  # Adjust columns width
                with col1:
                    st.subheader("💰 Live Crypto Prices")
                    st.dataframe(prices_df.style.format({"Price": "{:.2f}"}), height=300, width=500)

                with col2:
                    st.subheader("📈 Price Chart")
                    if not prices_df.empty:
                        fig_price = px.bar(prices_df, x="Crypto", y="Price", text="Price", 
                                           color="Crypto", title="Crypto Prices", height=400)
                        fig_price.update_layout(showlegend=False, template="plotly_dark")  # Dark theme
                        st.plotly_chart(fig_price, use_container_width=True)

    elif message.topic == "crypto_sentiment":
        sentiment = message.value
        new_row = pd.DataFrame([sentiment])  # Convert to DataFrame
        sentiment_df = pd.concat([new_row, sentiment_df], ignore_index=True)  # Append new row

        # Update sentiment table and chart in columns layout
        if page == "Sentiment Analysis":
            with sentiment_placeholder.container():
                col1, col2 = st.columns([3, 2])  # Adjust columns width
                with col1:
                    st.subheader("📰 Latest Crypto Sentiment")
                    st.dataframe(sentiment_df.tail(10), height=300)

                with col2:
                    st.subheader("📊 Sentiment Distribution")
                    sentiment_counts = sentiment_df["Sentiment"].value_counts()
                    
                    if not sentiment_counts.empty:
                        fig_sentiment = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, 
                                               title="Sentiment Distribution", height=400, template="plotly_dark")
                        st.plotly_chart(fig_sentiment, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by the Crypto Insights Team")
