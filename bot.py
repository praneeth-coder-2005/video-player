import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import BOT_TOKEN
from downloader import download_file, get_copy_type
import traceback
from tqdm import tqdm
import psutil  # For system performance information

# Initialize Flask app
app = Flask(__name__)

# WARNING: Using global variable to hold the updater
updater = Updater(BOT_TOKEN)

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

        # Get the file type
        mime_type = get_copy_type(local_path)
        print(f"Detected File Type: {mime_type}")

        update.message.reply_text('Uploading...')
        
        file_size = os.path.getsize(local_path)

        with open(local_path, 'rb') as file:
            # Use tqdm to show upload progress while loading the file
            with tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading', 
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]") as bar:
                
                file_content = file.read()  # Read the entire file content
                context.bot.send_document(chat_id=update.effective_chat.id, document=file_content,
                                          timeout=120, 
                                          disable_notification=True)

                # Update the progress bar
                bar.update(file_size)

                # Show system performance stats
                cpu_percent = psutil.cpu_percent()
                ram_info = psutil.virtual_memory()
                free_ram = ram_info.available / (1024 * 1024)  # Convert to MB
                processed_mb = file_size / (1024 * 1024)  # Total Size in MB

                print(f"├ Uploaded: {processed_mb:.2f}MB")
                print(f"├ Total Size: {file_size / (1024 * 1024):.2f}MB")
                print(f"├ CPU: {cpu_percent}% | RAM: {ram_info.percent}% | FREE: {free_ram:.2f}MB")

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
    return '', 200  # Return succes
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Assign port for deployment
    app.run(host='0.0.0.0', port=port)  # Start the Flask app

    # Start the bot using polling
    # Uncomment this line if you want to use polling instead of webhooks
    # updater.start_polling()
