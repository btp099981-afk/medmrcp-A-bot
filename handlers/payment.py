from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID



# =========================
# تفعيل انتظار إثبات الدفع
# =========================

async def request_payment_proof(
    update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    context.user_data[
        "waiting_payment_proof"
    ] = True



    await query.edit_message_text(

        "📤 Send your payment proof image now.\n\n"
        "After verification your Premium plan will be activated."

    )



# =========================
# استقبال صورة الدفع
# =========================

async def receive_payment_proof(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not context.user_data.get(
        "waiting_payment_proof"
    ):

        return



    user = update.effective_user



    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(

            "💎 New Premium Payment Proof\n\n"

            f"Name: {user.first_name}\n"

            f"Username: @{user.username}\n"

            f"ID: {user.id}"

        )

    )



    context.user_data[
        "waiting_payment_proof"
    ] = False



    await update.message.reply_text(

        "✅ Payment proof sent successfully.\n"
        "Waiting for verification."

  )
