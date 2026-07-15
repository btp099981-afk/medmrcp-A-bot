from telegram import Update
from telegram.ext import ContextTypes


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_message = update.message.text

    if not user_message:
        return

    response = (
        "🩺 MedMRCP AI Bot\n\n"
        "I received your message:\n"
        f"{user_message}\n\n"
        "Use /start to open the medical menu."
    )

    await update.message.reply_text(response)
