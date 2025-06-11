import requests

# Replace with your real values
TELEGRAM_TOKEN = "8012672180:AAH_IJ2s-paMNlq_uzbA38U2nxcZp4h5x0Y"
CHAT_ID = "6562108377"

def send_love_message(name="Maa or Papa"):
    message = f"💛 {name} just pressed the 'I MISS YOU' button on HomeGPT!"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    
    response = requests.post(url, data=payload)
    return response.ok
