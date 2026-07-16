import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from core.database import get_user, get_setting
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
                "⭐ Premium",
                callback_data="premium"
            )
        ],

        [
            InlineKeyboardButton(
                "👤 My Account",
                callback_data="account"
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
# الحساب
# =========================

def account_info(user_id):

    user = get_user(
        user_id
    )


    if not user:

        return "User not found."


    plan = "Free"

    if user[4]:

        plan = user[4].capitalize()


    phone = "Not added"

    if user[3]:

        phone = user[3]


    return (

        "👤 My Account\n\n"

        f"Name: {user[2]}\n"

        f"Phone: {phone}\n"

        f"Plan: {plan}\n"

        f"Join date: {user[5]}"

    )



# =========================
# Premium
# =========================

def premium_info():

    price = get_setting(
        "premium_price"
    )


    payment = get_setting(
        "payment_account"
    )


    return (

        "⭐ Premium Plan\n\n"

        f"💰 Price: {price}\n\n"

        "💳 Payment Account:\n"

        f"{payment}\n\n"

        "Send payment proof to activate Premium."

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


   
