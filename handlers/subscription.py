from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from core.database import (
    get_setting,
    create_payment_request,
    get_user
)

from config import ADMIN_ID



# =========================
# قائمة Premium
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
    ) or "Not set"


    bank = get_setting(
        "payment_account"
    ) or "Not set"


    whop = get_setting(
        "whop_link"
    ) or "Not set"



    await query.edit_message_text(

        "⭐ Premium Plan\n\n"

        f"💰 Price: {price}\n\n"

        "🏦 Bank Transfer:\n"

        f"{bank}\n\n"

        "🪙 USDT Payment:\n"

        f"{whop}\n\n"

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

        "⭐ Premium Subscription\n\n"

        "Complete payment using one of the methods above.\n\n"

        "Then send your payment proof."

    )



# =========================
# طلب إثبات الدفع
# =========================

async def payment_proof(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_payment_proof"
    ] = True


    await query.edit_message_text(

        "📤 Send your payment proof now.\n\n"
        "You can send a screenshot or payment details."

    )



# =========================
# حفظ إثبات الدفع
# =========================

async def save_payment_proof(update, context):

    if not context.user_data.get(
        "waiting_payment_proof"
    ):

        return


    user = update.effective_user


    proof = update.message.text


    create_payment_request(

        user.id,

        proof

    )


    context.user_data[
        "waiting_payment_proof"
    ] = False



    await update.message.reply_text(

        "✅ Payment proof received.\n\n"
        "Waiting for admin approval."

    )



    await context.bot.send_message(

        ADMIN_ID,

        "🔔 New Premium Request\n\n"

        f"Name: {user.first_name}\n"

        f"Username: @{user.username}\n"

        f"ID: {user.id}\n\n"

        "Check payment request."

    )



# =========================
# ربط زر Premium
# =========================

def get_subscription_handler():

    return CallbackQueryHandler(

        premium_page,

        pattern="^premium$"

    )
