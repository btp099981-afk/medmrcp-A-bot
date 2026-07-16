import os

from dotenv import load_dotenv

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


from core.database import (
    create_database,
    add_user,
    get_user
)


from handlers.menu import (
    get_main_menu,
    get_menu_handler
)


from handlers.chat import (
    handle_message
)


from handlers.admin import (
    get_admin_handler,
    get_payment_account_handler,
    save_payment_account
)


from handlers.profile import (
    request_phone,
    save_phone
)



# =========================
# Load environment
# =========================

load_dotenv()

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)



# =========================
# Start command
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    add_user(
        user.id,
        user.username,
        user.first_name
    )


    user_data = get_user(
        user.id
    )


    plan = "Free"


    if user_data:

        if len(user_data) > 4 and user_data[4]:

            plan = user_data[4].capitalize()



    await update.message.reply_text(

        f"👋 Welcome {user.first_name}\n\n"

        "🩺 DrBillAcademy\n\n"

        f"📌 Plan: {plan}\n\n"

        "Choose a section:",

        reply_markup=get_main_menu()

    )



# =========================
# Main
# =========================

def main():


    if not BOT_TOKEN:

        print(
            "BOT_TOKEN missing"
        )

        return



    create_database()



    app = Application.builder().token(
        BOT_TOKEN
    ).build()



    # Start

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )



    # Admin

    app.add_handler(
        get_admin_handler()
    )


    app.add_handler(
        get_payment_account_handler()
    )



    # Payment account text

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            save_payment_account

        )

    )



    # Phone

    app.add_handler(

        MessageHandler(

            filters.CONTACT,

            save_phone

        )

    )



    # Menu

    app.add_handler(
        get_menu_handler()
    )



    # Normal chat

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            handle_message

        )

    )



    print(
        "DrBillAcademy Bot is running..."
    )


    app.run_polling()



if __name__ == "__main__":

    main()
