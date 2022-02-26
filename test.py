from telegram import Update
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import sqlite3

with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()
db_file = "C:/Users/Jacky/Repo/HW0228-Telegram-Bot/content.sqlite"

CONSENT = -1
NAME, GENDER, AGE, SCHOOL, CONTROL1, CONTROL2, CONTROL3, FAV1, FAV2, FAV3, HATE1, HATE2, HATE3 = range(13)
user_data = {}


def update_db():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata(Name,Gender,Location) VALUES(?,?,?)", [user_data[0], user_data[1], user_data[2]])
    print('Db updated!')
    conn.commit()


def start_handler(update: Update, context):
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text(
        '''Hello! We are a group from HW0228 Scientific Communication, and we are conducting an experiment to find out if genres of music can affect the learning of an undergraduate student. 
The experiement will contain 3 tests, which will be repeated 3 times, in different conditions. It will not take more than 15 mins in total.
Before we begin, do you allow us to use the data that we will be collecting from you?''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes or No?'
        ),
    )
    print('end of start_handler')
    return CONSENT


def consent_handler(update: Update, context):
    print('start of consent_handler')
    update.message.reply_text(
        'We are glad you are able to help us do this experiment! Can we get your name please?',
    )
    return NAME


def no_consent_handler(update: Update, context):
    update.message.reply_text(
        'Thanks for using the bot! Good bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def name_handler(update: Update, context):
    print('start of name_handler')
    user_data[NAME] = update.message.text
    update.message.reply_text("Enter your gender")

    return GENDER


def gender_handler(update: Update, context):
    user_data[GENDER] = update.message.text
    update.message.reply_text("enter ur age")

    return AGE


def age_handler(update: Update, context):
    user_data[AGE] = update.message.text

    update.message.reply_text(f"registered successfully, you are {user_data[NAME]}, {user_data[GENDER]}, "
                              f"{user_data[AGE]}")
    update_db()

    return ConversationHandler.END


def cancel_handler(update: Update, context):
    update.message.reply_text(
        'Thanks for using the bot! Good bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CONSENT: [MessageHandler(Filters.regex('^(Yes|No)$'), consent_handler)],
            NAME: [MessageHandler(Filters.text, name_handler)],
            GENDER: [MessageHandler(Filters.text, gender_handler)],
            AGE: [MessageHandler(Filters.text, age_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)],
    )

    dp.add_handler(conv_handler)

    print('Bot running..')

    updater.start_polling()
    updater.idle()


main()
