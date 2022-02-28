from telegram import Update
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import sqlite3

with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()
db_file = 'C:/Users/Jacky/Repo/HW0228-Telegram-Bot/content.sqlite'


CONSENT, NAME, GENDER, AGE, SCHOOL, FAV, HATE, CONTROL1, CONTROL2, CONTROL3, FAV1, FAV2, FAV3, HATE1, HATE2, HATE3 = range(16)
test1 = 'https://10fastfingers.com'
test2 = 'https://www.mathsisfun.com'
test3 = 'https://www.memorylosstest.com/digit-span/'
user_data = {}


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
    return CONSENT


def consent_handler(update: Update, context):
    update.message.reply_text(
        'We are glad you are able to help us do this experiment! Can we get your name please?',
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


def no_consent_handler(update: Update, context):
    update.message.reply_text(
        'No consent. Thanks for using the bot! Good bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def name_handler(update: Update, context):
    user_data[NAME] = update.message.text
    update.message.reply_text('Enter your gender')
    return GENDER


def gender_handler(update: Update, context):
    user_data[GENDER] = update.message.text
    update.message.reply_text('enter your age')
    return AGE


def age_handler(update: Update, context):
    user_data[AGE] = update.message.text
    update.message.reply_text('what school (ntu, smu, nus, etc)')
    return SCHOOL


def school_handler(update: Update, context):
    user_data[SCHOOL] = update.message.text
    update.message.reply_text('''genres of music:
1. rock
2. a
3. b
4. c
5. d
6. e
7. 
8.
9.
    ''')
    update.message.reply_text('please choose your fav genre (num)')
    return FAV


def fav_handler(update: Update, context):
    user_data[FAV] = update.message.text
    update.message.reply_text('wlease choose your least fav genre (num)')
    return HATE


def hate_handler(update: Update, context):
    user_data[HATE] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. typing')
    update.message.reply_text('use this link: ' + test1)
    update.message.reply_text('once done, please reply your wpm')
    return CONTROL1


def control1_handler(update: Update, context):
    user_data[CONTROL1] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. math')
    update.message.reply_text('use this link: ' + test2)
    update.message.reply_text('once done, please reply your math score')
    return CONTROL2


def control2_handler(update: Update, context):
    user_data[CONTROL2] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. memory')
    update.message.reply_text('use this link: ' + test3)
    update.message.reply_text('once done, please reply your memory score')
    return CONTROL3


def control3_handler(update: Update, context):
    user_data[CONTROL3] = update.message.text
    update.message.reply_text('we will now start with the fav experiment. fav music. typing')
    update.message.reply_text('use this link: ' + test1)
    update.message.reply_text('once done, please reply your wpm')
    return FAV1


def fav1_handler(update: Update, context):
    user_data[FAV1] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. math')
    update.message.reply_text('use this link: ' + test2)
    update.message.reply_text('once done, please reply your math score')
    return FAV2


def fav2_handler(update: Update, context):
    user_data[FAV2] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. memory')
    update.message.reply_text('use this link: ' + test3)
    update.message.reply_text('once done, please reply your memory score')
    return FAV3


def fav3_handler(update: Update, context):
    user_data[FAV3] = update.message.text
    update.message.reply_text('we will now start with the hate experiment. hate music. typing')
    update.message.reply_text('use this link: ' + test1)
    update.message.reply_text('once done, please reply your wpm')
    return HATE1


def hate1_handler(update: Update, context):
    user_data[HATE1] = update.message.text
    update.message.reply_text('we will now start with the hate experiment. hate music. math')
    update.message.reply_text('use this link: ' + test2)
    update.message.reply_text('once done, please reply your math score')
    return HATE2


def hate2_handler(update: Update, context):
    user_data[HATE2] = update.message.text
    update.message.reply_text('we will now start with the hate experiment. hate music. memory')
    update.message.reply_text('use this link: ' + test3)
    update.message.reply_text('once done, please reply your memory score')
    return HATE3


def hate3_handler(update: Update, context):
    user_data[HATE3] = update.message.text
    update.message.reply_text('Thank you so much for your time. we have come to the end of our experiment. have a nice day!')
    #update_db()
    return ConversationHandler.END


def cancel_handler(update: Update, context):
    update.message.reply_text(
        'Thanks for using the bot! Good bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def update_db():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata(Name,Gender,Location) VALUES(?,?,?)", [user_data[0], user_data[1], user_data[2]])
    print('Db updated!')
    conn.commit()
    

def main():
    updater = Updater(token=BOT_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CONSENT: [MessageHandler(Filters.regex('^(Yes)$'), consent_handler), MessageHandler(Filters.regex('^(No)$'), no_consent_handler)],
            NAME: [MessageHandler(Filters.text, name_handler)],
            GENDER: [MessageHandler(Filters.text, gender_handler)],
            AGE: [MessageHandler(Filters.text, age_handler)],
            SCHOOL: [MessageHandler(Filters.text, school_handler)],
            FAV: [MessageHandler(Filters.text, fav_handler)],
            HATE: [MessageHandler(Filters.text, hate_handler)],
            CONTROL1: [MessageHandler(Filters.text, control1_handler)],
            CONTROL2: [MessageHandler(Filters.text, control2_handler)],
            CONTROL3: [MessageHandler(Filters.text, control3_handler)],
            FAV1: [MessageHandler(Filters.text, fav1_handler)],
            FAV2: [MessageHandler(Filters.text, fav2_handler)],
            FAV3: [MessageHandler(Filters.text, fav3_handler)],
            HATE1: [MessageHandler(Filters.text, hate1_handler)],
            HATE2: [MessageHandler(Filters.text, hate2_handler)],
            HATE3: [MessageHandler(Filters.text, hate3_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)],
    )

    dp.add_handler(conv_handler)

    print('Bot running..')

    updater.start_polling()
    updater.idle()


main()
