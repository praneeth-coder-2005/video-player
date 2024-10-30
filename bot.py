import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import BOT_TOKEN
from downloader import download_file, get_copy_type
import traceback
from tqdm import tqdm
import psutil  # For system performance information

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
