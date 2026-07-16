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

    return InlineKeyboardMarkup(keyboard)



# =========================
# فتح لوحة الإدارة
# =========================

async def admin_panel(update, context):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    if user_id != ADMIN_ID:

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
# زر تغيير الحساب
# =========================

async def change_payment_account(update, context):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    if user_id != ADMIN_ID:

        return



    await query.edit_message_text(

        "💳 Send the new payment account number."

    )


    context.user_data["waiting_payment_account"] = True



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
