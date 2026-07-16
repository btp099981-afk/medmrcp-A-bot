import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


# =========================
# القائمة الرئيسية
# =========================

def get_main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "🫀 Cardiology",
                callback_data="cardiology"
            ),
            InlineKeyboardButton(
                "🫁 Respiratory",
                callback_data="respiratory"
            ),
        ],
        [
            InlineKeyboardButton(
                "🧠 Neurology",
                callback_data="neurology"
            ),
            InlineKeyboardButton(
                "🍽 Gastroenterology",
                callback_data="gastro"
            ),
        ],
        [
            InlineKeyboardButton(
                "🩺 Renal System",
                callback_data="renal"
            ),
        ],
        [
            InlineKeyboardButton(
                "📚 History Taking",
                callback_data="history"
            ),
            InlineKeyboardButton(
                "📝 MCQ Practice",
                callback_data="mcq"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# قراءة المحتوى
# =========================

def load_content(file_name):

    path = os.path.join(
        "content",
        "internal_medicine",
        file_name
    )

    if not os.path.exists(path):
        return "⚠️ Content file not found."

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# =========================
# التعامل مع الأزرار
# =========================

async def menu_callback(update, context):

    query = update.callback_query

    await query.answer()

    section = query.data


    if section == "history":

        text = load_content(
            "history_taking.txt"
        )

    elif section == "mcq":

        text = (
            "📝 MCQ Practice\n\n"
            "Question bank coming soon."
        )

    else:

        sections = {

            "cardiology":
                "🫀 Cardiology\n\nContent will be loaded soon.",

            "respiratory":
                "🫁 Respiratory\n\nContent will be loaded soon.",

            "neurology":
                "🧠 Neurology\n\nContent will be loaded soon.",

            "gastro":
                "🍽 Gastroenterology\n\nContent will be loaded soon.",

            "renal":
                "🩺 Renal System\n\nContent will be loaded soon.",
        }

        text = sections.get(
            section,
            "Choose a section from the menu."
        )


    await query.edit_message_text(
        text=text,
        reply_markup=get_main_menu()
    )


# =========================
# Handler
# =========================

def get_menu_handler():

    return CallbackQueryHandler(
        menu_callback
    )
