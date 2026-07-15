import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")


# ==========================
# Start Menu
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("❤️ Cardiovascular", callback_data="cardio")],
        [InlineKeyboardButton("🫁 Respiratory", callback_data="respiratory")],
        [InlineKeyboardButton("🧠 Neurology", callback_data="neurology")],
        [InlineKeyboardButton("🍽 Gastrointestinal", callback_data="gi")],
        [InlineKeyboardButton("🫘 Renal", callback_data="renal")]
    ]

    await update.message.reply_text(
        "Welcome to MedMRCP AI 🩺\n\nChoose a system:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================
# Buttons
# ==========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    # Cardiovascular
    if query.data == "cardio":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🫀 Chest Pain",
                    callback_data="chest_pain"
                )
            ],
            [
                InlineKeyboardButton(
                    "💓 Palpitations",
                    callback_data="palpitations"
                )
            ],
            [
                InlineKeyboardButton(
                    "😵 Syncope",
                    callback_data="syncope"
                )
            ]
        ]

        await query.edit_message_text(
            "❤️ Cardiovascular Cases:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # Chest Pain Case
    elif query.data == "chest_pain":

        context.user_data["case"] = "chest_pain"

        await query.edit_message_text(
            "🫀 Chest Pain Case\n\n"
            "Patient: Ahmed\n"
            "Age: 55 years old\n"
            "Gender: Male\n\n"
            "Chief complaint:\n"
            "Chest pain\n\n"
            "Start taking history."
        )


    # Other cases (temporary)
    elif query.data in ["palpitations", "syncope"]:

        await query.edit_message_text(
            "This case will be added soon."
        )


    else:

        await query.edit_message_text(
            f"Selected: {query.data}"
        )



# ==========================
# Patient Answers
# ==========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()


    if context.user_data.get("case") == "chest_pain":

        if "name" in text:

            await update.message.reply_text(
                "My name is Ahmed."
            )

        elif "age" in text or "old" in text:

            await update.message.reply_text(
                "I am 55 years old."
            )

        elif "start" in text or "when" in text:

            await update.message.reply_text(
                "It started 2 hours ago."
            )

        else:

            await update.message.reply_text(
                "I am the patient. Please continue your history taking."
            )

    else:

        await update.message.reply_text(
            "Choose a clinical case first."
        )



# ==========================
# Run Bot
# ==========================

def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler("start", start)
    )


    app.add_handler(
        CallbackQueryHandler(button_handler)
    )


    app.add_handler(
        MessageHandler(filters.TEXT, handle_message)
    )


    print("Bot is running...")


    app.run_polling()



if __name__ == "__main__":
    main()
