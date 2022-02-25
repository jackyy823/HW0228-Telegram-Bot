#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import sys
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import sqlite3
from telegram import ReplyKeyboardMarkup
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def loadDB():
    # Creates SQLite database to store info.
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.executescript('''CREATE TABLE IF NOT EXISTS userdata
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
    Name TEXT,
    Gender TEXT,
    Location TEXT,
    Description TEXT);'''
    )
    conn.commit()
    conn.close()

def updateTable(conn, userdata):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO userdata(Name,Gender,Location,Description)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, userdata)
    conn.commit()
    return cur.lastrowid

# def checkUser(update, user_data):
#     # Checks if user has visited the bot before
#     # If yes, load data of user
#     # If no, then create a new entry in database
#     conn = sqlite3.connect('content.sqlite')
#     cur = conn.cursor()
#     conn.text_factory = str
#     if len(cur.execute('''SELECT id FROM userdata WHERE id = ?
#             ''', (update.message.from_user.id,)).fetchall())>0:
#         c=cur.execute('''SELECT Name FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
#         user_data['Name']=c[0]
#         c=cur.execute('''SELECT Age FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
#         user_data['Age']=c[0]
#         c=cur.execute('''SELECT Address FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
#         user_data['Address']=c[0]
#         c=cur.execute('''SELECT Amount FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
#         user_data['Amount']=c[0]
#         print('Past user')
#     else:
#         cur.execute('''INSERT OR IGNORE INTO userdata (id, firstname) VALUES (?, ?)''', \
#         (update.message.from_user.id, update.message.from_user.first_name,))
#         print('New user')
#     conn.commit()
#     conn.close()

# def updateUser(category, text, update):
#     # Updates user info as inputted.
#     conn = sqlite3.connect('content.sqlite')
#     cur = conn.cursor()
#     conn.text_factory = str
#     # Update SQLite database as needed.
#     cur.execute('''UPDATE OR IGNORE userdata SET {} = ? WHERE id = ?'''.format(category), \
#         (text, update.message.from_user.id,))
#     conn.commit()
#     conn.close()
#
# def facts_to_str(user_data):
#     facts = list()
#
#     for key, value in user_data.items():
#         facts.append('{} - {}'.format(key, value))
#
#     return "\n".join(facts).join(['\n', '\n'])
#
#
# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
#
# def received_information(bot, update, user_data):
#     text = update.message.text
#     category = user_data['choice']
#     user_data[category] = text
#     updateUser(category, text, update)
#     del user_data['choice']
#
#     update.message.reply_text("Neat! Just so you know, this is what you already told me:"
#                               "{}"
#                               "You can tell me more, or change your opinion on something.".format(
#         facts_to_str(user_data)), reply_markup=markup)
#     return CHOOSING
#
# reply_keyboard = [['Name', 'Gender'],
#                   ['Location', 'Other'],
#                   ['Done']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I see! Please send me a photo of yourself, '
        'so I know what you look like, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! At last, tell me something about yourself.'
    )

    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'You seem a bit paranoid! At last, tell me something about yourself.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5194037439:AAHbD9f6i745hsG-Rocpnt0JGDcbjBVKVSQ")

    # Create data in db
    database = "/Users/jacky/Repo/telegram-bot-store-info-sqlite-database/content.sqlite"
    conn = create_connection(database)


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    data = (GENDER, '-1', '-1', '-1')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    with conn:
        print('in here')
        updateTable(conn, data)
        print('updated table')


if __name__ == '__main__':
    loadDB()
    main()

