from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from core.database import update_phone



# =========================
# طلب رقم الهاتف
# =========================

async def request_phone(
    update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [

        [
            KeyboardButton(
                "📱 Share My Phone Number",
                request_contact=True
            )
        ]

    ]


    await update.message.reply_text(

        "Please share your phone number to complete your profile.",

        reply_markup=ReplyKeyboardMarkup(

            keyboard,

            resize_keyboard=True,

            one_time_keyboard=True

        )

    )



# =========================
# حفظ رقم الهاتف
# =========================

async def save_phone(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    contact = update.message.contact


    if not contact:

        return



    user_id = update.effective_user.id


    phone = contact.phone_number



    update_phone(

        user_id,

        phone

    )



    await update.message.reply_text(

        "✅ Phone number saved successfully.",

    )
