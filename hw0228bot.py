from telegram import Update
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import sqlite3

with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()
db_file = 'C:/Users/Jacky/Repo/Survey-Telegram-Bot/content.db'

CONSENT, ENVIRONMENT, NAME, GENDER, AGE, SCHOOL, Q1, Q2, Q3, Q4, FAV, HATE, CONTROL1, CONTROL2, CONTROL3, FAV1, FAV2, FAV3, HATE1, HATE2, HATE3 = range(21)
tests = ['https://tinyurl.com/hw0228customtyping', 'https://arithmetic.zetamac.com/game?key=5709eab0', 'https://timodenk.com/blog/digit-span-test-online-tool/']
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
        '''Hello! We are a group of students from NTU, collecting experiment results for our module, HW0228 Scientific Communication. \
We are conducting an experiment to investigate the effect of different genres of music as a study aid on undergraduate \
students. The experiment will consists of 3 tests, namely a typing test, a simple arithmetic test, and a digit span test. \
We will repeat these 3 experiments under 3 conditions. Fret not if you are confused, the bot will guide you along the \
experiment.
This experiment should take around 20 minutes in total. Before we begin, do you consent to your data being collected?''',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return CONSENT


def consent_handler(update: Update, context):
    user_data[CONSENT] = update.message.text
    reply_keyboard = [['Yes, I am ready.', 'No, I will continue this later.']]

    update.message.reply_text(
        '''Thank you for your consent. Before we begin, this test would require you to be in a quiet environment free of distractions. \
We also require you to be on your laptop/desktop for one of the test. Please also ensure that you have your preferred choice of \
headphone with you now to listen to the music. Thank you.'''
    )
    update.message.reply_text('Are you ready?',
    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return ENVIRONMENT


def no_consent_handler(update: Update, context):
    update.message.reply_text(
        'No consent given. Thanks for using our bot! Goodbye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def environment_handler(update: Update, context):
    user_data[ENVIRONMENT] = update.message.text
    update.message.reply_text(
        '''Thank you for helping us to take this test. Before we begin, we we give you a brief introduction on the tests that \
you will be taking. 

1. 2 Minutes Typing Test:
You will be given 2 minutes to type as many words as you can as per shown on the screen. To move on to the next word \
press <SPACEBAR>.
2. Mental Arithmetic Test:
You will be given 2 minutes to perform as many simple mental arithmetic questions as possible. The questions consist of \
addition and subtraction questions for numbers less than 100, as well as multiplication tables up to 12. The site will \
automatically display a new question upon the correct input. 
3. Digit Span Test:
This is a simple memory test where numbers will be read out to you and flashed in sequence. Your job is to remember \
the sequence of numbers and type it out. The test advances in difficulty upon the completion of each level.

You will repeat the three tests under three conditions:
    a. Controlled (No music)
    b. With your favourite music
    c. With your least favourite music''')
   
    update.message.reply_text(
        'We will now commence the experiment. Please enter your name: ', reply_markup=ReplyKeyboardRemove()
    )
    return NAME


def no_environment_handler(update: Update, context):
    update.message.reply_text(
        'We hope to see you again when you are ready. Goodbye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def name_handler(update: Update, context):
    user_data[NAME] = update.message.text
    reply_keyboard = [['Male', 'Female', 'Other']]
    
    update.message.reply_text('Please enter your gender: ',
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return GENDER


def gender_handler(update: Update, context):
    user_data[GENDER] = update.message.text
    update.message.reply_text('Please enter your age (integer): ', reply_markup=ReplyKeyboardRemove())
    return AGE


def age_handler(update: Update, context):
    user_data[AGE] = update.message.text
    update.message.reply_text('Please enter your tertiary institution (e.g. NUS, NTU, SMU, SUTD etc.)')
    return SCHOOL


def school_handler(update: Update, context): 
    user_data[SCHOOL] = update.message.text
    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text('In the past 2 weeks, did you study while listening to the music?',
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return Q1


def q1_handler(update: Update, context): 
    user_data[Q1] = update.message.text
    reply_keyboard = [['1', '2', '3', '4', '5', 'NA']]

    update.message.reply_text('''If you input yes for the previous question, indicate on a scale of 1-5, \
rate how frequent that you listen to music while studying. Otherwise, input NA
        ''', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return Q2


def q2_handler(update: Update, context): 
    user_data[Q2] = update.message.text
    reply_keyboard = [['1', '2', '3', '4', '5', '6']]

    update.message.reply_text('''Why do you choose to listen to music while studying? Choose the most applicable \
answer to you:
1. It helps me to focus better.
2. It improves my mood. 
3. It makes learning less dull.
4. It helps me to focus better. 
5. It improves my endurance while studying. 
6. Others.''', 
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return Q3


def q2_handler_alternative(update: Update, context): 
    user_data[Q2] = update.message.text
    reply_keyboard = [['1', '2', '3', '4', '5', '6']]

    update.message.reply_text('''Why do you choose not to listen to music while studying? Choose the most applicable \
answer to you:
1. It distracts me from my work. 
2. It fouls my mood.
3. It doesn't help me with my memorization and consolidation of knowledge. 
4. I do not listen to music usually.
5. My endurance is worse when I listen to music. 
6. Others.''', 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )
    return Q3


def q3_handler(update:Update, context):
    user_data[Q3] = update.message.text
    update.message.reply_text('On the range from -100% to 100% How much more/less productive do you find \
yourself when studying while listening to music (eg. 50%, -30%)?', reply_markup=ReplyKeyboardRemove())
    return Q4


def q4_handler(update: Update, context):
    user_data[Q4] = update.message.text
    reply_keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9']]

    update.message.reply_text(f''' Here are the genres of music available for your selection:
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
    update.message.reply_text('Please enter your favourite music genre (integer) to listen to when you study: ',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Select a number between 1 and 9')
    ),
    return FAV


def fav_handler(update: Update, context):
    user_data[FAV] = update.message.text
    reply_keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9']]
    update.message.reply_text('Please enter your least favourite music genre (integer) to listen to when you study: ',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Select a number between 1 and 9')
    )
    return HATE


def hate_handler(update: Update, context):
    user_data[HATE] = update.message.text
    update.message.reply_text('We will now begin with the control experiment without music. Please ensure that you are in a quiet \
enviroment. When you are ready, please click on the link to start the typing test.', reply_markup=ReplyKeyboardRemove(),)
    update.message.reply_text('2 Minutes Typing Test: ' + tests[0])
    update.message.reply_text('Once done, please enter your WPM')
    return CONTROL1


def control1_handler(update: Update, context):
    user_data[CONTROL1] = update.message.text
    update.message.reply_text('(CONTROL) Please click on the link to start the arithmetic test.')
    update.message.reply_text('2 Minutes Arithmetic test: ' + tests[1])
    update.message.reply_text('Once done, please enter your math score')
    return CONTROL2


def control2_handler(update: Update, context):
    user_data[CONTROL2] = update.message.text
    update.message.reply_text('''For the digit span test, we will need you to connect your headphone device. Please ensure that it \
is of a comfortable volume.''')
    update.message.reply_text('(CONTROL) Please click on the link to start the digit span test.')
    update.message.reply_text('Digit Span Test test: ' + tests[2])
    update.message.reply_text('Once done, please enter your memory score')
    return CONTROL3


def control3_handler(update: Update, context):
    user_data[CONTROL3] = update.message.text
    update.message.reply_text('''You will now repeat the three experiments while listening to your favourite genre of music while \
studying. Please click on the link to the playlist and skip the advertisement.''')
    update.message.reply_text(f'Link to {genre[int(user_data[FAV])-1]} playlist: ' + music[int(user_data[FAV])-1])
    update.message.reply_text('When you are ready, please click on the link to start the typing test.')
    update.message.reply_text('2 Minutes Typing Test: ' + tests[0])
    update.message.reply_text('Once done, please enter your WPM')
    return FAV1


def fav1_handler(update: Update, context):
    user_data[FAV1] = update.message.text
    update.message.reply_text('(FAVOURITE MUSIC) Please click on the link to start the arithmetic test.')
    update.message.reply_text('2 Minutes Arithmetic test: ' + tests[1])
    update.message.reply_text('Once done, please enter your math score')
    return FAV2


def fav2_handler(update: Update, context):
    user_data[FAV2] = update.message.text
    update.message.reply_text('(FAVOURITE MUSIC) Please click on the link to start the digit span test.')
    update.message.reply_text('Digit Span Test test: ' + tests[2])
    update.message.reply_text('Once done, please enter your memory score')
    return FAV3


def fav3_handler(update: Update, context):
    user_data[FAV3] = update.message.text
    update.message.reply_text('''You will now repeat the three experiments while listening to your least preferred genre of music while \
studying. Please click on the link to the playlist and skip the advertisement.''')
    update.message.reply_text(f'Link to {genre[int(user_data[HATE])-1]} playlist: ' + music[int(user_data[HATE])-1])
    update.message.reply_text('When you are ready, please click on the link to start the typing test.')
    update.message.reply_text('2 Minutes Typing Test: ' + tests[0])
    update.message.reply_text('Once done, please enter your WPM')
    return HATE1


def hate1_handler(update: Update, context):
    user_data[HATE1] = update.message.text
    update.message.reply_text('(LEAST PREFERRED MUSIC) Please click on the link to start the arithmetic test.')
    update.message.reply_text('2 Minutes Arithmetic test: ' + tests[1])
    update.message.reply_text('Once done, please enter your math score')
    return HATE2


def hate2_handler(update: Update, context):
    user_data[HATE2] = update.message.text
    update.message.reply_text('(LEAST PREFERRED MUSIC) Please click on the link to start the digit span test.')
    update.message.reply_text('Digit Span Test test: ' + tests[2])
    update.message.reply_text('Once done, please enter your memory score')
    return HATE3


def hate3_handler(update: Update, context):
    user_data[HATE3] = update.message.text
    update.message.reply_text('''Thank you so much for your time. we have come to the end of our experiment. Your help is \
greatly appreciated.''')
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
    ENVIRONMENT TEXT,
    NAME TEXT, 
    GENDER TEXT,
    AGE TEXT,
    SCHOOL TEXT,
    Q1 TEXT,
    Q2 TEXT,
    Q3 TEXT,
    Q4 TEXT,
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
    cur.execute('INSERT INTO userdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8], user_data[9], user_data[10], user_data[11], user_data[12], user_data[13], user_data[14], user_data[15], user_data[16], user_data[17], user_data[18], user_data[19], user_data[20]))
    print('Db updated!')
    conn.commit()
    

def main():

    updater = Updater(token=BOT_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CONSENT: [MessageHandler(Filters.regex('^(Yes|yes)$'), consent_handler), MessageHandler(Filters.regex('^(No|no)$'), no_consent_handler)],
            ENVIRONMENT: [MessageHandler(Filters.regex('Yes.*'), environment_handler), MessageHandler(Filters.regex('No.*'), no_environment_handler)],
            NAME: [MessageHandler(Filters.text, name_handler)],
            GENDER: [MessageHandler(Filters.text, gender_handler)],
            AGE: [MessageHandler(Filters.regex('^[0-9]'), age_handler)],
            SCHOOL: [MessageHandler(Filters.text, school_handler)],
            Q1: [MessageHandler(Filters.text, q1_handler)],
            Q2: [MessageHandler(Filters.regex('^[1-5]'), q2_handler), MessageHandler(Filters.regex('^(NA)$'), q2_handler_alternative)],
            Q3: [MessageHandler(Filters.regex('^[1-6]'), q3_handler)],
            Q4: [MessageHandler(Filters.regex('^-?[0-9]'), q4_handler)],
            FAV: [MessageHandler(Filters.regex('^[1-9]'), fav_handler)],
            HATE: [MessageHandler(Filters.regex('^[1-9]'), hate_handler)],
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
