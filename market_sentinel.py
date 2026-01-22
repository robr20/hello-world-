import requests
import os
from openai import OpenAI # Or your preferred 2026 LLM SDK

# Configuration
NEWS_API_KEY = "your_alpha_vantage_key"
TELEGRAM_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
llm_client = OpenAI(api_key="your_ai_key")

def fetch_financial_news():
    # Fetching news with built-in sentiment analysis
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=CRYPTO:BTC,AAPL&apikey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json().get('feed', [])[:5] # Get top 5 stories

def analyze_with_market_sentinel(news_items):
    raw_text = str(news_items)
    
    # This is where your system prompt from before lives
    completion = llm_client.chat.completions.create(
        model="gpt-4o", # Or Gemini-1.5-Pro
        messages=[
            {"role": "system", "content": "You are Market Sentinel... [Insert Full Prompt Here]"},
            {"role": "user", "content": f"Analyze these raw headlines: {raw_text}"}
        ]
    )
    return completion.choices[0].message.content

def push_to_telegram(report):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": report, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# Execution Loop
if __name__ == "__main__":
    news = fetch_financial_news()
    if news:
        report = analyze_with_market_sentinel(news)
        push_to_telegram(report)
        print("Report pushed to device!")
