import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Debug print statement to verify if the token is loaded correctly
print(f"Loaded TELEGRAM_BOT_TOKEN: {BOT_TOKEN}")

if not BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")
