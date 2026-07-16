from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from config import ADMIN_ID

from core.database import (
    update_setting,
    get_pending_payments,
    update_payment_status,
    update_plan
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
                "🔔 Payment Requests",
                callback_data="payment_requests"
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
# طلبات الدفع
# =========================

async def payment_requests(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        return



    requests = get_pending_payments()


    if not requests:

        await query.edit_message_text(
            "No pending payment requests."
        )

        return



    for request in requests:

        request_id = request[0]

        user_id = request[1]

        proof = request[2]


        keyboard = [

            [
                InlineKeyboardButton(
                    "✅ Approve Premium",
                    callback_data=f"approve_{request_id}_{user_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject_{request_id}"
                )
            ]

        ]


        await context.bot.send_message(

            ADMIN_ID,

            "🔔 Premium Payment Request\n\n"

            f"User ID: {user_id}\n\n"

            f"Proof:\n{proof}",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )

        )


    await query.edit_message_text(
        "✅ Payment requests sent."
    )



# =========================
# الموافقة
# =========================

async def approve_payment(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        return



    data = query.data.split("_")


    request_id = int(data[1])

    user_id = int(data[2])


    update_payment_status(

        request_id,

        "approved"

    )


    update_plan(

        user_id,

        "premium"

    )


    await context.bot.send_message(

        user_id,

        "🎉 Congratulations!\n\n"
        "Your Premium plan is now active."

    )


    await query.edit_message_text(

        "✅ User upgraded to Premium."

    )



# =========================
# الرفض
# =========================

async def reject_payment(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        return



    request_id = int(
        query.data.split("_")[1]
    )


    update_payment_status(

        request_id,

        "rejected"

    )


    await query.edit_message_text(

        "❌ Payment rejected."

    )



# =========================
# تغيير حساب الدفع
# =========================

async def change_payment_account(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_payment_account"
    ] = True


    await query.edit_message_text(

        "💳 Send new payment account."

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



    update_setting(

        "payment_account",

        update.message.text

    )


    context.user_data[
        "waiting_payment_account"
    ] = False



    await update.message.reply_text(

        "✅ Payment account updated."

    )



# =========================
# الربط
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


def get_payment_requests_handler():

    return CallbackQueryHandler(

        payment_requests,

        pattern="^payment_requests$"

    )


def get_approve_handler():

    return CallbackQueryHandler(

        approve_payment,

        pattern="^approve_"

    )


def get_reject_handler():

    return CallbackQueryHandler(

        reject_payment,

        pattern="^reject_"

        )
