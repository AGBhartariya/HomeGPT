import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

def ask_homegpt(prompt):
    try:
        # Choose the model (e.g., "gemini-1.5-pro-latest")
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            f"You are a very warm, friendly family assistant named HomeGPT who provides solutions to every question in a very respectful manner and cares for people. Make it in the best way possible.\n\nUser: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"
