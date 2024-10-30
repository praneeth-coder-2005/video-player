import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import BOT_TOKEN
from downloader import download_file
import traceback

# Ensure the downloads directory exists
DOWNLOAD_DIR = './downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me a URL and I will download the file and send it back to you.')

def leech(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    print(f"Received URL: {url}")  # Debugging output

    # Basic URL validation
    if not url.startswith("http://") and not url.startswith("https://"):
        update.message.reply_text("Please provide a valid URL that starts with 'http://' or 'https://'.")
        return

    try:
        update.message.reply_text('Downloading...')
        local_path = download_file(url, DOWNLOAD_DIR)

        if local_path is None:
            update.message.reply_text('Failed to download the file. Please check the URL and try again.')
            return

        update.message.reply_text('Uploading...')
        with open(local_path, 'rb') as file:
            update.message.reply_document(document=file)

        # Cleanup
        os.remove(local_path)

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        traceback.print_exc()  # Print the full stack trace
        update.message.reply_text(f"Failed to process the request: {str(e)}")

def main():
    try:
        print(f"Using BOT_TOKEN: {BOT_TOKEN}")  # Debug print statement
        updater = Updater(BOT_TOKEN)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, leech))

        updater.start_polling()
        updater.idle()

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
