from telegram import Update
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import sqlite3

NAME, GENDER, AGE = range(3)
user_data = {}


def start_handler(update: Update, context):
    update.message.reply_text(
        "Enter your name:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


def name_handler(update: Update, context):
    user_data[NAME] = update.message.text

    update.message.reply_text("Enter your gender")

    return GENDER


def age_handler(update: Update, context):
    user_data[GENDER] = update.message.text
    update.message.reply_text("enter ur age")

    return AGE


def finish_handler(update: Update, context):
    user_data[AGE] = update.message.text

    update.message.reply_text(f"registered successfully, you are {user_data[NAME]}, {user_data[GENDER]}, "
                              f"{user_data[AGE]}")
    print("dict of user_data")
    print(user_data)

    conn = sqlite3.connect("C:/Users/Jacky/Repo/HW0228-Telegram-Bot/content.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata(Name,Gender,Location) VALUES(?,?,?)", [user_data[0], user_data[1], user_data[2]])
    print(user_data[0])
    print('updated db')
    conn.commit()
    return ConversationHandler.END


def cancel_handler(update: Update, context):
    print("bye")


def main():
    updater = Updater(
        token="5194037439:AAGEhR3P8eHgRdCwpjCIurLe2aqZGlJyziI",
        use_context=True,
    )

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_handler),
        ],
        states={
            NAME: [MessageHandler(Filters.all, name_handler)],
            GENDER: [MessageHandler(Filters.all, age_handler)],
            AGE: [MessageHandler(Filters.all, finish_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
    )

    dp.add_handler(conv_handler)
    print('bot running')
    updater.start_polling()
    updater.idle()


main()