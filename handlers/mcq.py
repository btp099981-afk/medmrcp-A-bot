import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler



# =========================
# قائمة MCQ
# =========================

def get_mcq_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "📝 MRCP Part 1 MCQ",
                callback_data="mcq_part1"
            )
        ],

        [
            InlineKeyboardButton(
                "🩺 Clinical Cases",
                callback_data="mcq_cases"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# قراءة الملف
# =========================

def read_mcq_file(filename):

    path = os.path.join(
        "content",
        filename
    )


    if not os.path.exists(path):

        return "⚠️ MCQ content not found."



    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# =========================
# فتح MCQ
# =========================

async def mcq_callback(update, context):

    query = update.callback_query

    await query.answer()



    files = {

        "mcq_part1":
        "mrcp_part1_mcq.txt",


        "mcq_cases":
        "mrcp_clinical_cases.txt"

    }



    data = query.data



    if data in files:

        text = read_mcq_file(
            files[data]
        )


        await query.edit_message_text(
            text
        )



# =========================
# Handler
# =========================

def get_mcq_handler():

    return CallbackQueryHandler(

        mcq_callback,

        pattern="^mcq_"

  )
