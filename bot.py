import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from downloader import download_file
from gdrive import upload_file_to_drive
from config import BOT_TOKEN, DRIVE_FOLDER_ID

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me a URL to mirror it onto Google Drive.')

def mirror(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    filename = os.path.basename(url)
    
    # Download file
    update.message.reply_text('Downloading...')
    local_path = f'./downloads/{filename}'
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    download_file(url, local_path)
    
    # Upload to Google Drive
    update.message.reply_text('Uploading to Google Drive...')
    file_id = upload_file_to_drive(local_path, filename, DRIVE_FOLDER_ID)
    
    # Respond with Google Drive link
    link = f'https://drive.google.com/file/d/{file_id}/view'
    update.message.reply_text(f'File uploaded to Google Drive: {link}')
    
    # Cleanup
    os.remove(local_path)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mirror))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
