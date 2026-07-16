from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from config import ADMIN_ID

from core.database import update_setting



# =========================
# لوحة الإدارة
# =========================

def get_admin_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "💳 Change Payment Account",
                callback_data="change_payment_account"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 Change Premium Price",
                callback_data="change_price"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# فتح لوحة الإدارة
# =========================

async def admin_panel(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        await query.edit_message_text(
            "❌ Access denied."
        )

        return



    await query.edit_message_text(

        "⚙️ DrBillAcademy Admin Panel\n\n"
        "Choose an action:",

        reply_markup=get_admin_menu()

    )



# =========================
# تغيير حساب الدفع
# =========================

async def change_payment_account(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        return



    context.user_data[
        "waiting_payment_account"
    ] = True



    await query.edit_message_text(

        "💳 Send the new payment account."

    )



# =========================
# حفظ حساب الدفع
# =========================

async def save_payment_account(update, context):

    if update.effective_user.id != ADMIN_ID:

        return



    if not context.user_data.get(
        "waiting_payment_account"
    ):

        return



    account = update.message.text


    update_setting(
        "payment_account",
        account
    )


    context.user_data[
        "waiting_payment_account"
    ] = False



    await update.message.reply_text(

        "✅ Payment account updated."

    )



# =========================
# تغيير سعر الاشتراك
# =========================

async def change_price(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        return



    context.user_data[
        "waiting_price"
    ] = True



    await query.edit_message_text(

        "💰 Send the new premium price."

    )



# =========================
# حفظ السعر
# =========================

async def save_price(update, context):

    if update.effective_user.id != ADMIN_ID:

        return



    if not context.user_data.get(
        "waiting_price"
    ):

        return



    price = update.message.text


    update_setting(
        "premium_price",
        price
    )


    context.user_data[
        "waiting_price"
    ] = False



    await update.message.reply_text(

        "✅ Premium price updated."

    )



# =========================
# ربط الأزرار
# =========================

def get_admin_handler():

    return CallbackQueryHandler(

        admin_panel,

        pattern="^admin$"

    )



def get_payment_account_handler():

    return CallbackQueryHandler(

        change_payment_account,

        pattern="^change_payment_account$"

    )



def get_price_handler():

    return CallbackQueryHandler(

        change_price,

        pattern="^change_price$"

    )
