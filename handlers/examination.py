import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler



# =========================
# قائمة Examination
# =========================

def get_examination_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🫀 Cardiovascular Examination",
                callback_data="exam_cardiovascular"
            )
        ],

        [
            InlineKeyboardButton(
                "🫁 Respiratory Examination",
                callback_data="exam_respiratory"
            )
        ],

        [
            InlineKeyboardButton(
                "🧠 Neurological Examination",
                callback_data="exam_neurology"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# قراءة ملف الفحص
# =========================

def read_exam_file(filename):

    path = os.path.join(
        "content",
        filename
    )


    if not os.path.exists(path):

        return "⚠️ Examination content not found."



    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# =========================
# فتح Examination
# =========================

async def examination_callback(update, context):

    query = update.callback_query

    await query.answer()



    data = query.data



    files = {

        "exam_cardiovascular":
        "exam_cardiovascular.txt",


        "exam_respiratory":
        "exam_respiratory.txt",


        "exam_neurology":
        "exam_neurology.txt"

    }



    if data in files:

        text = read_exam_file(
            files[data]
        )


        await query.edit_message_text(
            text
        )



# =========================
# Handler
# =========================

def get_examination_handler():

    return CallbackQueryHandler(

        examination_callback,

        pattern="^exam_"

      )
