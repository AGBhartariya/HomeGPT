import streamlit as st
import requests

def send_telegram_message(user_message, sender_name):
    # Securely get bot token and chat ID from secrets
    bot_token = st.secrets["TELEGRAM_BOT_TOKEN"]
    chat_id = st.secrets["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Include sender's name in message text
    text = f"📩 Message from {sender_name}:\n{user_message}"
    
    data = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print("Telegram send error:", e)
        return False
