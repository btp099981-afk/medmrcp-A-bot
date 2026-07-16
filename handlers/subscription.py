from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from core.database import (
    get_setting,
    create_payment_request
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

    return InlineKeyboardMarkup(keyboard)



# =========================
# صفحة Premium
# =========================

async def premium_page(update, context):

    query = update.callback_query

    await query.answer()


    price = get_setting(
        "premium_price"
    ) or "Not set"


    account = get_setting(
        "payment_account"
    ) or "Not set"


    usdt = get_setting(
        "whop_link"
    ) or "Not set"



    await query.edit_message_text(

        "👑 Premium Plan\n\n"

        f"💰 Price: {price}\n\n"

        f"🏦 Payment Account:\n{account}\n\n"

        f"🪙 USDT / Whop:\n{usdt}\n\n"

        "Choose payment option:",

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

        "Complete payment then send proof."

    )



# =========================
# إرسال إثبات الدفع
# =========================

async def payment_proof(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_payment_proof"
    ] = True



    await query.edit_message_text(

        "📤 Send payment proof now."

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

        "✅ Payment proof received.\n"
        "Waiting for admin approval."

    )



    await context.bot.send_message(

        ADMIN_ID,

        "🔔 New Premium payment request\n\n"

        f"User ID: {user.id}\n"

        f"Username: @{user.username}\n\n"

        f"Proof:\n{proof}"

    )



# =========================
# Handlers
# =========================

def get_subscription_handler():

    return CallbackQueryHandler(

        premium_page,

        pattern="^premium$"

    )



def get_subscribe_handler():

    return CallbackQueryHandler(

        subscribe,

        pattern="^subscribe$"

    )



def get_payment_proof_handler():

    return CallbackQueryHandler(

        payment_proof,

        pattern="^payment_proof$"

)
