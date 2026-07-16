import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from config import ADMIN_ID
from core.database import get_user



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
            )
        ],

        [
            InlineKeyboardButton(
                "🧠 Neurology",
                callback_data="neurology"
            ),
            InlineKeyboardButton(
                "🍽 Gastro",
                callback_data="gastro"
            )
        ],

        [
            InlineKeyboardButton(
                "🩺 Renal System",
                callback_data="renal"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 History Taking",
                callback_data="history_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "🩺 Clinical Examination",
                callback_data="exam_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 MRCP Practice",
                callback_data="mcq_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "👑 Premium",
                callback_data="premium"
            ),

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
# الحساب
# =========================

def account_info(user_id):

    user = get_user(
        user_id
    )


    if not user:

        return "User not found."


    plan = "Free"


    if len(user) > 4 and user[4]:

        plan = user[4].capitalize()


    return (

        "👤 My Account\n\n"

        f"Name: {user[2]}\n"

        f"Plan: {plan}"

    )



# =========================
# التعامل مع الأزرار
# =========================

async def menu_callback(update, context):

    query = update.callback_query

    await query.answer()


    section = query.data



    if section in [

        "cardiology",
        "respiratory",
        "neurology",
        "gastro",
        "renal"

    ]:

        from handlers.content import get_content_menu


        await query.edit_message_text(

            f"📚 {section.capitalize()}\n\n"
            "Choose content type:",

            reply_markup=get_content_menu(
                section
            )

        )

        return



    elif section == "history_menu":

        from handlers.history import get_history_menu


        await query.edit_message_text(

            "📋 History Taking",

            reply_markup=get_history_menu()

        )

        return



    elif section == "exam_menu":

        from handlers.examination import get_examination_menu


        await query.edit_message_text(

            "🩺 Clinical Examination",

            reply_markup=get_examination_menu()

        )

        return



    elif section == "mcq_menu":

        from handlers.mcq import get_mcq_menu


        await query.edit_message_text(

            "📝 MRCP Practice",

            reply_markup=get_mcq_menu()

        )

        return



    elif section == "account":

        await query.edit_message_text(

            account_info(
                query.from_user.id
            )

        )

        return



    elif section == "premium":

        await query.edit_message_text(

            "👑 Premium\n\n"
            "Premium features coming soon."

        )

        return



    else:

        await query.edit_message_text(

            "Coming soon..."

        )



# =========================
# Handler
# =========================

def get_menu_handler():

    return CallbackQueryHandler(

        menu_callback,

        pattern="^(cardiology|respiratory|neurology|gastro|renal|history_menu|exam_menu|mcq_menu|account|premium)$"

    )
