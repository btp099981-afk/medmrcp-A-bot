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
    get_price_handler,
    save_payment_account,
    save_price
)


from handlers.profile import (
    request_phone,
    save_phone
)



# =========================
# تحميل المتغيرات
# =========================

load_dotenv()

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)



# =========================
# البداية
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


    if user_data and user_data[4]:

        plan = user_data[4].capitalize()



    await update.message.reply_text(

        f"👋 أهلاً بك {user.first_name}\n\n"

        "🩺 MedMRCP AI\n\n"

        f"📌 Your plan: {plan}\n\n"

        "Choose a section:",

        reply_markup=get_main_menu(
            user.id
        )

    )



# =========================
# التشغيل
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



    # Admin buttons

    app.add_handler(
        get_admin_handler()
    )


    app.add_handler(
        get_payment_account_handler()
    )


    app.add_handler(
        get_price_handler()
    )



    # Admin text input

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            save_payment_account

        )

    )


    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            save_price

        )

    )



    # Phone

    app.add_handler(

        MessageHandler(

            filters.Regex(
                "^📱 Share My Phone Number$"
            ),

            request_phone

        )

    )


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



    # Chat

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            handle_message

        )

    )



    print(
        "MedMRCP AI Bot is running..."
    )


    app.run_polling()



if __name__ == "__main__":

    main()
