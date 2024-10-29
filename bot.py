from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import BOT_TOKEN

# Start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me a URL to mirror it.')

# Mirror handler for responding with the received URL
def mirror(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    
    # Just acknowledge the URL received
    response_message = f"URL received: {url}\n(Mirroring functionality is currently not implemented)"
    update.message.reply_text(response_message)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    
    # Register command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mirror))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
