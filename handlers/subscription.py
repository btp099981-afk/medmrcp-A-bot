from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from core.database import get_setting



# =========================
# قائمة الاشتراك
# =========================

def get_subscription_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "💳 Subscribe Now",
                callback_data="subscribe"
            )
        ],

        [
            InlineKeyboardButton(
                "📤 Send Payment Proof",
                callback_data="payment_proof"
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
# شاشة Premium
# =========================

async def premium_page(update, context):

    query = update.callback_query

    await query.answer()


    price = get_setting(
        "premium_price"
    )


    payment = get_setting(
        "payment_account"
    )


    await query.edit_message_text(

        "⭐ Premium Plan\n\n"

        f"💰 Price: {price}\n\n"

        f"💳 Payment Account:\n{payment}\n\n"

        "Choose an option:",

        reply_markup=get_subscription_menu()

    )



# =========================
# زر الاشتراك
# =========================

async def subscribe(update, context):

    query = update.callback_query

    await query.answer()


    await query.edit_message_text(

        "💳 To subscribe:\n\n"
        "Send payment then press "
        "📤 Send Payment Proof."

    )



# =========================
# إثبات الدفع
# =========================

async def payment_proof(update, context):

    query = update.callback_query

    await query.answer()


    await query.edit_message_text(

        "📤 Send your payment proof "
        "as a photo or message."

    )



# =========================
# ربط الأزرار
# =========================

def get_subscription_handler():

    return CallbackQueryHandler(

        premium_page,

        pattern="^premium$"

  )
