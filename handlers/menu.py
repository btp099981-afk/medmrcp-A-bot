from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================
# القائمة الرئيسية
# =========================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "❤️ Cardiovascular",
                callback_data="cardio"
            )
        ],

        [
            InlineKeyboardButton(
                "🫁 Respiratory",
                callback_data="respiratory"
            )
        ],

        [
            InlineKeyboardButton(
                "🧠 Neurology",
                callback_data="neurology"
            )
        ],

        [
            InlineKeyboardButton(
                "🩺 Gastrointestinal",
                callback_data="gi"
            )
        ],

        [
            InlineKeyboardButton(
                "🫘 Renal",
                callback_data="renal"
            )
        ],

        [
            InlineKeyboardButton(
                "⭐ Premium Plan",
                callback_data="premium"
            )
        ],

        [
            InlineKeyboardButton(
                "👤 My Account",
                callback_data="account"
            )
        ]

    ]


    return InlineKeyboardMarkup(keyboard)
