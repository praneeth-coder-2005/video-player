import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from downloader import download_file, get_copy_type
import traceback

# Replace with your actual bot token (keep it secure in production)
BOT_TOKEN = '7820729855:AAG_ph7Skh4SqGxIWYYcRNigQqCKdnVW354'

# Initialize Flask app
app = Flask(__name__)

# Set up the Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Ensure the downloads directory exists
DOWNLOAD_DIR = './downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return "Telegram Bot is running!", 200  # Optional root route for health check

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me a URL and I will download the file and send it back to you.')

async def leech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    print(f"Received URL: {url}")  # Debug output

    # Basic URL validation
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("Please provide a valid URL that starts with 'http://' or 'https://'.")
        return

    try:
        await update.message.reply_text('Downloading...')
        local_path = download_file(url, DOWNLOAD_DIR)

        if local_path is None:
            await update.message.reply_text('Failed to download the file. Please check the URL and try again.')
            return

        # Get the file type
        mime_type = get_copy_type(local_path)
        print(f"Detected File Type: {mime_type}")

        await update.message.reply_text('Uploading...')

        file_size = os.path.getsize(local_path)

        with open(local_path, 'rb') as file:
            content = file.read()  # Read the entire file content
            await context.bot.send_document(chat_id=update.effective_chat.id, document=content, timeout=120, disable_notification=True)

        # Cleanup
        os.remove(local_path)

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        traceback.print_exc()  # Print the full stack trace
        await update.message.reply_text(f"Failed to process the request: {str(e)}")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()  # Get incoming update
    update = Update.de_json(json_data, application.bot)  # Create an Update object
    application.dispatcher.process_update(update)  # Process the update
    return '', 200  # Return success status

# Add command and message handlers
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, leech))

# Set webhook for the Telegram bot
def set_webhook():
    webhook_url = 'https://video-player-4o4x.onrender.com/webhook'
    application.bot.set_webhook(webhook_url)

# Run the bot using Flask
if __name__ == '__main__':
    set_webhook()  # Set the webhook before starting the server
    port = int(os.environ.get('PORT', 5000))  # Assign port for deployment
    app.run(host='0.0.0.0', port=port)
