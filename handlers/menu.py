from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


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


async def menu_callback(update, context):
    query = update.callback_query
    await query.answer()

    section = query.data

    sections = {
        "cardiology": "🫀 Cardiology\n\nContent will be loaded soon.",
        "respiratory": "🫁 Respiratory\n\nContent will be loaded soon.",
        "neurology": "🧠 Neurology\n\nContent will be loaded soon.",
        "gastro": "🍽 Gastroenterology\n\nContent will be loaded soon.",
        "renal": "🩺 Renal System\n\nContent will be loaded soon.",
        "history": "📚 History Taking\n\nClinical history training.",
        "mcq": "📝 MCQ Practice\n\nQuestion bank coming soon.",
    }

    text = sections.get(
        section,
        "Choose a section from the menu."
    )

    await query.edit_message_text(
        text=text,
        reply_markup=get_main_menu()
    )


def get_menu_handler():
    return CallbackQueryHandler(menu_callback)
