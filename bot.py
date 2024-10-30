import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import BOT_TOKEN
from downloader import download_file, get_copy_type
import traceback
import psutil  # For system performance information
from tqdm import tqdm

# Initialize Flask app
app = Flask(__name__)

# Set up the Updater
updater = Updater(BOT_TOKEN)

# Ensure the downloads directory exists
DOWNLOAD_DIR = './downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return "Telegram Bot is running!", 200  # Optional root route for health check

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me a URL and I will download the file and send it back to you.')

def leech(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    print(f"Received URL: {url}")  # Debug output

    # Basic URL validation
    if not url.startswith(("http://", "https://")):
        update.message.reply_text("Please provide a valid URL that starts with 'http://' or 'https://'.")
        return

    try:
        update.message.reply_text('Downloading...')
        local_path = download_file(url, DOWNLOAD_DIR)

        if local_path is None:
            update.message.reply_text('Failed to download the file. Please check the URL and try again.')
            return

        # Get the file type
        mime_type = get_copy_type(local_path)
        print(f"Detected File Type: {mime_type}")

        update.message.reply_text('Uploading...')
        
        file_size = os.path.getsize(local_path)

        with open(local_path, 'rb') as file:
            # Use tqdm to show upload progress while loading the file
            content = file.read()  # Read the entire file content
            context.bot.send_document(chat_id=update.effective_chat.id, document=content,
                                      timeout=120, 
                                      disable_notification=True)

        # Cleanup
        os.remove(local_path)

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        traceback.print_exc()  # Print the full stack trace
        update.message.reply_text(f"Failed to process the request: {str(e)}")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()  # Get incoming update
    update = Update.de_json(json_data, updater.bot)  # Create an Update object
    updater.dispatcher.process_update(update)  # Process the update
    return '', 200  # Return success status

# Add command and message handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, leech))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Assign port for deployment
    app.run(host='0.0.0.0', port=port) 
