import requests
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    name = update.message.from_user.first_name
    update.message.reply_text('Hi ' + name+', what should I search the dictionary for?')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def word(update, context):
    """Find word meaning."""
    word_id = update.message.text
    language = "en-gb"
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
    r = requests.get(url, headers={"app_id": "XXXXXX", "app_key": "XXXXXXX"}).json()
    if r == {'error': 'No entry found matching supplied source_lang, word and provided filters'}:
        update.message.reply_text("Sorry! Word not found.")
    else:
        data = r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        update.message.reply_text("Meaning of " + word_id.upper() + ": " + data)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater("XXXXXXX", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, word))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
