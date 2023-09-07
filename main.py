from bot.telegram_bot import start_bot
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')


if __name__ == "__main__":
    if API_KEY:
        start_bot(API_KEY)
    else:
        print("Error: No se encontró la API key.")
