import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from core.database import get_user


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
                "🍽 Gastro",
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

        [
            InlineKeyboardButton(
                "👤 My Account",
                callback_data="account"
            )
        ]

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
# زر الحساب
# =========================

def account_info(user_id):

    user = get_user(user_id)


    if not user:

        return "User not found."


    plan = user[3].capitalize()
    join_date = user[4]


    return (

        "👤 My Account\n\n"

        f"Name: {user[2]}\n"

        f"Plan: {plan}\n"

        f"Join date: {join_date}"

    )



# =========================
# التعامل مع الأزرار
# =========================

async def menu_callback(update, context):

    query = update.callback_query

    await query.answer()


    section = query.data


    files = {

        "history": "history_taking.txt",
        "cardiology": "cardiology.txt",
        "respiratory": "respiratory.txt",
        "neurology": "neurology.txt",
        "gastro": "gastro.txt",
        "renal": "renal.txt",

    }


    if section in files:

        text = load_content(
            files[section]
        )


    elif section == "account":

        text = account_info(
            query.from_user.id
        )


    elif section == "mcq":

        text = (
            "📝 MCQ Practice\n\n"
            "Coming soon."
        )


    else:

        text = "Choose a section."



    await query.edit_message_text(

        text=text,

        reply_markup=get_main_menu()

    )



def get_menu_handler():

    return CallbackQueryHandler(
        menu_callback
)
