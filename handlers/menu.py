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
            ),
        ],

        [
            InlineKeyboardButton(
                "💎 Premium",
                callback_data="premium"
            ),
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
# قراءة الإعدادات
# =========================

def get_setting(key):

    import sqlite3

    conn = sqlite3.connect(
        "medmrcp.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM settings WHERE key=?",
        (key,)
    )

    result = cursor.fetchone()

    conn.close()


    if result:
        return result[0]

    return "Not set"



# =========================
# الحساب
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
# Premium
# =========================

def premium_info():

    account = get_setting(
        "payment_account"
    )


    return (

        "💎 DrBillAcademy Premium\n\n"

        "Get access to:\n"

        "✅ Clinical Cases\n"

        "✅ Advanced Medical Content\n"

        "✅ MCQ Practice\n\n"

        "Subscription payment:\n\n"

        f"Account Number:\n{account}\n\n"

        "After payment send your proof."

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


    elif section == "premium":

        text = premium_info()


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
