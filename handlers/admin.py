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
                "💰 Change Premium Price",
                callback_data="change_price"
            )
        ],

        [
            InlineKeyboardButton(
                "🪙 Change USDT Link",
                callback_data="change_whop"
            )
        ],

        [
            InlineKeyboardButton(
                "🔔 Payment Requests",
                callback_data="payment_requests"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)



# =========================
# فتح الإدارة
# =========================

async def admin_panel(update, context):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:

        return


    await query.edit_message_text(

        "⚙️ Admin Panel\n\n"
        "Choose an action:",

        reply_markup=get_admin_menu()

    )



# =========================
# تغيير الحساب البنكي
# =========================

async def change_payment_account(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_payment_account"
    ] = True


    await query.edit_message_text(
        "💳 Send new payment account:"
    )



# =========================
# تغيير السعر
# =========================

async def change_price(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_price"
    ] = True


    await query.edit_message_text(
        "💰 Send new Premium price:"
    )



# =========================
# تغيير رابط Whop
# =========================

async def change_whop(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_whop"
    ] = True


    await query.edit_message_text(
        "🪙 Send new USDT / Whop link:"
    )



# =========================
# حفظ إعدادات الإدارة
# =========================

async def save_admin_setting(update, context):

    if update.effective_user.id != ADMIN_ID:

        return


    text = update.message.text


    if context.user_data.get(
        "waiting_payment_account"
    ):

        update_setting(
            "payment_account",
            text
        )

        context.user_data[
            "waiting_payment_account"
        ] = False


        await update.message.reply_text(
            "✅ Payment account updated."
        )



    elif context.user_data.get(
        "waiting_price"
    ):

        update_setting(
            "premium_price",
            text
        )

        context.user_data[
            "waiting_price"
        ] = False


        await update.message.reply_text(
            "✅ Premium price updated."
        )



    elif context.user_data.get(
        "waiting_whop"
    ):

        update_setting(
            "whop_link",
            text
        )

        context.user_data[
            "waiting_whop"
        ] = False


        await update.message.reply_text(
            "✅ USDT/Whop link updated."
        )



# =========================
# طلبات الدفع
# =========================

async def payment_requests(update, context):

    query = update.callback_query

    await query.answer()


    requests = get_pending_payments()


    if not requests:

        await query.edit_message_text(
            "No pending requests."
        )

        return



    for item in requests:

        request_id = item[0]

        user_id = item[1]

        proof = item[2]


        keyboard = [

            [
                InlineKeyboardButton(
                    "✅ Approve",
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

            f"🔔 Payment Request\n\n"
            f"User: {user_id}\n\n"
            f"Proof:\n{proof}",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )

        )


# =========================
# الموافقة
# =========================

async def approve_payment(update, context):

    query = update.callback_query

    await query.answer()


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

        "🎉 Your Premium plan is active."

    )


    await query.edit_message_text(
        "✅ Approved."
    )



# =========================
# الرفض
# =========================

async def reject_payment(update, context):

    query = update.callback_query

    await query.answer()


    request_id = int(
        query.data.split("_")[1]
    )


    update_payment_status(
        request_id,
        "rejected"
    )


    await query.edit_message_text(
        "❌ Rejected."
    )



# =========================
# Handlers
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


def get_price_handler():

    return CallbackQueryHandler(
        change_price,
        pattern="^change_price$"
    )


def get_whop_handler():

    return CallbackQueryHandler(
        change_whop,
        pattern="^change_whop$"
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
