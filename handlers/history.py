import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler



# =========================
# قائمة History Taking
# =========================

def get_history_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "👤 Adult History",
                callback_data="history_adult"
            )
        ],

        [
            InlineKeyboardButton(
                "🫀 Cardiovascular History",
                callback_data="history_cardiovascular"
            )
        ],

        [
            InlineKeyboardButton(
                "🫁 Respiratory History",
                callback_data="history_respiratory"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# قراءة الملف
# =========================

def read_history_file(filename):

    path = os.path.join(
        "content",
        filename
    )


    if not os.path.exists(path):

        return "⚠️ History content not found."


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# =========================
# فتح History
# =========================

async def history_callback(update, context):

    query = update.callback_query

    await query.answer()


    data = query.data



    files = {

        "history_adult":
        "history_adult.txt",


        "history_cardiovascular":
        "history_cardiovascular.txt",


        "history_respiratory":
        "history_respiratory.txt"

    }



    if data in files:

        text = read_history_file(
            files[data]
        )


        await query.edit_message_text(
            text
        )



# =========================
# Handler
# =========================

def get_history_handler():

    return CallbackQueryHandler(

        history_callback,

        pattern="^history_"

  )
