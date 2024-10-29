import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import BOT_TOKEN
from downloader import download_file

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me a URL and I will download the file and send it back to you.')

def leech(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    
    try:
        # Determine the filename from the URL
        filename = url.split('/')[-1]
        local_path = f'./downloads/{filename}'

        # Download the file
        update.message.reply_text('Downloading...')
        download_file(url, local_path)
        
        # Send the file back to the user
        update.message.reply_text('Uploading...')
        update.message.reply_document(document=open(local_path, 'rb'))
        
        # Cleanup
        os.remove(local_path)
    except Exception as e:
        update.message.reply_text(f"Failed to download the file: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, leech))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
