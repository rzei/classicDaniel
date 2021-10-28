"""
A simple telegram bot that saves messages and resends them on request.
Quick fun projekt to mess with a friend who is abusing the delete message feature of telegram.
"""

# Libs

import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)



saved_messages = []
def new_message(update: Update, context: CallbackContext) -> None:
    # extract message
    message = update.message
    # get username
    username = message.from_user.name
    # check if correct username
    if username == '@gackolo':    
        # save message
        saved_messages.append(message)
        print("new message saved")


def get_log(update: Update, context: CallbackContext) -> None:
    # check arguments
    arg = context.args
    try:
        # get first argument
        arg = int(arg[0])
    except:
        # else default value
        arg = 5

    output = saved_messages[-arg:]
    msg = ""
    for e in output:
        msg += e.text + '\n\n'

    #msg += "\n #classicDaniel"
    context.bot.send_message(update.message.chat_id, msg)

once = True
def start(update: Update, context: CallbackContext) -> None:
    global once
    if once:
        msg = "Daaaamn Daniel, i am here to destroy your shitty habits ;)"
        context.bot.send_message(update.message.chat_id, msg)
        once = False

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    with open('token.txt') as f:
        token = f.read()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, new_message))
    dispatcher.add_handler(CommandHandler("classicDaniel", get_log))


    # Start the Bot
    updater.start_polling()

    print("Daniel is back online")


if __name__ == '__main__':
    main()
