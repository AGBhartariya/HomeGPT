import streamlit as st
import requests
def send_telegram_message(user_message):
    # Replace with your bot token and chat_id (your Telegram user ID)
    bot_token = st.secrets["TELEGRAM_BOT_TOKEN"]  # Store in Streamlit secrets for security
    chat_id = st.secrets["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": user_message
    }
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        return False
