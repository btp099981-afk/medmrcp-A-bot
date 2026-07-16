from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

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

        "💳 Complete payment first.\n\n"
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

        "📤 Please send your payment proof now."

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



    # إرسال إشعار للمدير

    await context.bot.send_message(

        ADMIN_ID,

        "🔔 New Premium Payment Request\n\n"

        f"Name: {user.first_name}\n"

        f"Username: @{user.username}\n"

        f"ID: {user.id}\n\n"

        "Please review the payment."

    )



# =========================
# ربط الأزرار
# =========================

def get_subscription_handler():

    return CallbackQueryHandler(

        premium_page,

        pattern="^premium$"

    )
