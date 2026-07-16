import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================
# قائمة نوع المحتوى
# =========================

def get_content_menu(system):

    keyboard = [

        [
            InlineKeyboardButton(
                "📖 Notes",
                callback_data=f"notes_{system}"
            )
        ],

        [
            InlineKeyboardButton(
                "🩺 Clinical Cases",
                callback_data=f"cases_{system}"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 MCQ Practice",
                callback_data=f"mcq_{system}"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back_menu"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# قراءة الملفات
# =========================

def read_content(path):

    if not os.path.exists(path):

        return "⚠️ Content not available yet."


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# =========================
# فتح المحتوى
# =========================

async def open_content(update, context):

    query = update.callback_query

    await query.answer()


    data = query.data.split("_")


    content_type = data[0]

    system = data[1]



    path = os.path.join(

        "content",

        system,

        f"{content_type}.txt"

    )



    text = read_content(
        path
    )



    await query.edit_message_text(

        text

    )



# =========================
# ربط handler
# =========================

from telegram.ext import CallbackQueryHandler


def get_content_handler():

    return CallbackQueryHandler(

        open_content,

        pattern="^(notes|cases|mcq)_"

    )
