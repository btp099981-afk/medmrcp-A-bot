from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from config import ADMIN_ID

from core.database import (
    add_discount,
    get_user_by_phone
)



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
                "🎁 Add Discount",
                callback_data="add_discount"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# شاشة اختيار الخصم
# =========================

def get_discount_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "10%",
                callback_data="discount_10"
            ),

            InlineKeyboardButton(
                "25%",
                callback_data="discount_25"
            )
        ],

        [
            InlineKeyboardButton(
                "50%",
                callback_data="discount_50"
            ),

            InlineKeyboardButton(
                "75%",
                callback_data="discount_75"
            )
        ],

        [
            InlineKeyboardButton(
                "100%",
                callback_data="discount_100"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="admin"
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
# بدء إضافة الخصم
# =========================

async def add_discount_menu(update, context):

    query = update.callback_query

    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return



    await query.edit_message_text(

        "🎁 Select discount percentage:",

        reply_markup=get_discount_menu()

    )



# =========================
# اختيار نسبة الخصم
# =========================

async def select_discount(update, context):

    query = update.callback_query

    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return



    percent = int(
        query.data.split("_")[1]
    )



    context.user_data[
        "discount_percent"
    ] = percent



    context.user_data[
        "waiting_discount_phone"
    ] = True



    await query.edit_message_text(

        f"🎁 Discount selected: {percent}%\n\n"
        "📱 Send user's phone number."

    )



# =========================
# استقبال رقم الهاتف للخصم
# =========================

async def save_discount(update, context):

    if update.effective_user.id != ADMIN_ID:

        return



    if not context.user_data.get(
        "waiting_discount_phone"
    ):

        return



    phone = update.message.text



    user = get_user_by_phone(
        phone
    )



    if not user:

        await update.message.reply_text(

            "❌ User not found."

        )

        return



    percent = context.user_data.get(
        "discount_percent",
        0
    )



    add_discount(

        user[0],

        percent

    )



    context.user_data[
        "waiting_discount_phone"
    ] = False



    await update.message.reply_text(

        "✅ Discount added successfully.\n\n"

        f"User: {user[2]}\n"

        f"Discount: {percent}%"

    )



# =========================
# طلب رقم الحساب الجديد
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

        "💳 Send the new payment account number."

    )



# =========================
# استقبال رقم الحساب
# =========================

async def save_payment_account(update, context):

    if update.effective_user.id != ADMIN_ID:

        return



    if not context.user_data.get(
        "waiting_payment_account"
    ):

        return



    account = update.message.text



    import sqlite3


    conn = sqlite3.connect(
        "medmrcp.db"
    )

    cursor = conn.cursor()


    cursor.execute(

        """
        INSERT OR REPLACE INTO settings
        (key,value)

        VALUES (?,?)
        """,

        (
            "payment_account",
            account
        )

    )


    conn.commit()

    conn.close()



    context.user_data[
        "waiting_payment_account"
    ] = False



    await update.message.reply_text(

        "✅ Payment account updated successfully."

    )



# =========================
# ربط لوحة الإدارة
# =========================

def get_admin_handler():

    return CallbackQuery
