from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from config import ADMIN_ID


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
        (key, value)

        VALUES (?, ?)
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
