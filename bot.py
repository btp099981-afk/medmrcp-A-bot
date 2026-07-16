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
# تحميل المتغيرات
# =========================

load_dotenv()

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)



# =========================
# أمر البداية
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

        "🩺 DrBillAcademy\n\n"

        f"📌 Your plan: {plan}\n\n"

        "Choose a section:",

        reply_markup=get_main_menu()

    )



# =========================
# تشغيل البوت
# =========================

def main():


    if not BOT_TOKEN:

        print("BOT_TOKEN غير موجود")

        return



    create_database()



    app = Application.builder().token(
        BOT_TOKEN
    ).build()



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



    # استقبال رقم الحساب من المدير

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            save_payment_account

        )

    )



    # طلب رقم الهاتف

    app.add_handler(

        MessageHandler(

            filters.Regex(
                "^📱 Share My Phone Number$"
            ),

            request_phone

        )

    )



    # حفظ رقم الهاتف

    app.add_handler(

        MessageHandler(

            filters.CONTACT,

            save_phone

        )

    )



    # القائمة

    app.add_handler(
        get_menu_handler()
    )



    # الرسائل العادية

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
