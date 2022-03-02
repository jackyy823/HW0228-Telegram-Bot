from telegram import Update
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import sqlite3

with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()
db_file = 'C:/Users/Jacky/Repo/Survey-Telegram-Bot/content.db'

CONSENT, NAME, GENDER, AGE, SCHOOL, FAV, HATE, CONTROL1, CONTROL2, CONTROL3, FAV1, FAV2, FAV3, HATE1, HATE2, HATE3 = range(16)
tests = ['https://10fastfingers.com', 'https://arithmetic.zetamac.com/game?key=5cccbe99', 'https://timodenk.com/blog/digit-span-test-online-tool/']
genre = ['Lo-fi', 'Classical', 'Pop', 'Blues', 'Jazz', 'Hip-Pop', 'Rock', 'Heavy Metal', 'Electronic Dance Music']
music = ['https://youtu.be/mT6c8tcv75Y', # Lo-fi
'https://youtu.be/RzEr66WYcm8', # Classical
'https://youtu.be/h_NiEKQauOM', # Pop
'https://youtu.be/SH3KlDlqu_k', # Blues
'https://youtu.be/o26qoCYLdS8', # Jazz
'https://youtu.be/OQLPUPC8pUM', # Hip-Pop
'https://youtu.be/26nsBfLXwSQ', # Rock
'https://youtu.be/Lmp2zJ7UNPM', # Heavy Metal
'https://youtu.be/1MHh6ykSlm8', # Electronic Dance Music
] 

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
    user_data[CONSENT] = update.message.text
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
    reply_keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9']]
    update.message.reply_text(f'''genres of music:
1. {genre[0]}
2. {genre[1]}
3. {genre[2]}
4. {genre[3]}
5. {genre[4]}
6. {genre[5]}
7. {genre[6]}
8. {genre[7]}
9. {genre[8]}
    ''')
    update.message.reply_text('please choose your fav genre (num)',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Select a number between 1 and 9')
    )
    return FAV


def fav_handler(update: Update, context):
    user_data[FAV] = update.message.text
    reply_keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9']]
    update.message.reply_text('please choose your least fav genre (num)',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Select a number between 1 and 9')
    )
    return HATE


def hate_handler(update: Update, context):
    user_data[HATE] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. typing', reply_markup=ReplyKeyboardRemove(),)
    update.message.reply_text('use this link: ' + tests[0])
    update.message.reply_text('once done, please reply your wpm')
    return CONTROL1


def control1_handler(update: Update, context):
    user_data[CONTROL1] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. math')
    update.message.reply_text('use this link: ' + tests[1])
    update.message.reply_text('once done, please reply your math score')
    return CONTROL2


def control2_handler(update: Update, context):
    user_data[CONTROL2] = update.message.text
    update.message.reply_text('we will now start with the control experiment. no music. memory')
    update.message.reply_text('use this link: ' + tests[2])
    update.message.reply_text('once done, please reply your memory score')
    return CONTROL3


def control3_handler(update: Update, context):
    user_data[CONTROL3] = update.message.text
    update.message.reply_text('we will now start with the fav experiment. fav music. typing')
    update.message.reply_text('use this link: ' + tests[0])
    update.message.reply_text('music vid: ' + music[int(user_data[FAV])-1])
    update.message.reply_text('once done, please reply your wpm')
    return FAV1


def fav1_handler(update: Update, context):
    user_data[FAV1] = update.message.text
    update.message.reply_text('we will now start with the fav experiment. fav music. math')
    update.message.reply_text('use this link: ' + tests[1])
    update.message.reply_text('once done, please reply your math score')
    return FAV2


def fav2_handler(update: Update, context):
    user_data[FAV2] = update.message.text
    update.message.reply_text('we will now start with the fav experiment. fav music. memory')
    update.message.reply_text('use this link: ' + tests[2])
    update.message.reply_text('once done, please reply your memory score')
    return FAV3


def fav3_handler(update: Update, context):
    user_data[FAV3] = update.message.text
    update.message.reply_text('we will now start with the hate experiment. hate music. typing')
    update.message.reply_text('use this link: ' + tests[0])
    update.message.reply_text('music vid: ' + music[int(user_data[HATE])-1])
    update.message.reply_text('once done, please reply your wpm')
    return HATE1


def hate1_handler(update: Update, context):
    user_data[HATE1] = update.message.text
    update.message.reply_text('we will now start with the hate experiment. hate music. math')
    update.message.reply_text('use this link: ' + tests[1])
    update.message.reply_text('once done, please reply your math score')
    return HATE2


def hate2_handler(update: Update, context):
    user_data[HATE2] = update.message.text
    update.message.reply_text('we will now start with the hate experiment. hate music. memory')
    update.message.reply_text('use this link: ' + tests[2])
    update.message.reply_text('once done, please reply your memory score')
    return HATE3


def hate3_handler(update: Update, context):
    user_data[HATE3] = update.message.text
    update.message.reply_text('Thank you so much for your time. we have come to the end of our experiment. have a nice day!')
    update_db()
    return ConversationHandler.END


def cancel_handler(update: Update, context):
    update.message.reply_text(
        'Thanks for using the bot! Good bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def update_db():
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    cur.executescript('''CREATE TABLE IF NOT EXISTS userdata
    (
    CONSENT TEXT, 
    NAME TEXT, 
    GENDER TEXT,
    AGE TEXT,
    SCHOOL TEXT,
    FAV TEXT,
    HATE TEXT,
    CONTROL1 TEXT,
    CONTROL2 TEXT,
    CONTROL3 TEXT,
    FAV1 TEXT,
    FAV2 TEXT,
    FAV3 TEXT,
    HATE1 TEXT,
    HATE2 TEXT,
    HATE3 TEXT);'''
    )
    cur.execute('INSERT INTO userdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8], user_data[9], user_data[10], user_data[11], user_data[12], user_data[13], user_data[14], user_data[15]))
    print('Db updated!')
    conn.commit()
    

def main():


    updater = Updater(token=BOT_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CONSENT: [MessageHandler(Filters.regex('^(Yes|yes)$'), consent_handler), MessageHandler(Filters.regex('^(No|no)$'), no_consent_handler)],
            NAME: [MessageHandler(Filters.text, name_handler)],
            GENDER: [MessageHandler(Filters.text, gender_handler)],
            AGE: [MessageHandler(Filters.regex('^[0-9]'), age_handler)],
            SCHOOL: [MessageHandler(Filters.text, school_handler)],
            FAV: [MessageHandler(Filters.regex('^[0-9]'), fav_handler)],
            HATE: [MessageHandler(Filters.regex('^[0-9]'), hate_handler)],
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
