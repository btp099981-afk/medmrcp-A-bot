import os
import sqlite3

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from core.database import get_user
from config import ADMIN_ID



# =========================
# القائمة الرئيسية
# =========================

def get_main_menu(user_id=None):

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
        ],

        [
            InlineKeyboardButton(
                "💎 Premium",
                callback_data="premium"
            )
        ]

    ]


    if user_id == ADMIN_ID:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⚙️ Admin Panel",
                    callback_data="admin"
                )
            ]
        )


    return InlineKeyboardMarkup(
        keyboard
    )



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

    conn = sqlite3.connect(
        "medmrcp.db"
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT value
        FROM settings
        WHERE key=?
        """,
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

    user = get_user(
        user_id
    )


    if not user:

        return "User not found."



    return (

        "👤 My Account\n\n"

        f"Name: {user[2]}\n"

        f"Plan: {user[3].capitalize()}\n"

        f"Join date: {user[4]}"

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

        "Features:\n"

        "✅ Clinical Cases\n"

        "✅ Advanced Medical Content\n"

        "✅ MCQ Practice\n\n"

        "Payment Account:\n"

        f"{account}\n\n"

        "After payment send your proof."

    )



# =========================
# التعامل مع الأزرار
# =========================

async def menu_callback(
    update,
    context
):

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

        return



    await query.edit_message_text(

        text=text,

        reply_markup=get_main_menu(
            query.from_user.id
        )

    )



def get_menu_handler():

    return CallbackQueryHandler(
        menu_callback
        )
