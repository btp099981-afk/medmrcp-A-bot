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


# تحميل المتغيرات
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================
# أمر البداية
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # تسجيل المستخدم في قاعدة البيانات
    add_user(
        user.id,
        user.username,
        user.first_name
    )

    user_data = get_user(user.id)

    plan = "Free"

    if user_data:
        plan = user_data[3].capitalize()


    await update.message.reply_text(
        f"👋 أهلاً بك {user.first_name}\n\n"
        "🩺 MedMRCP AI\n"
        "مساعدك للتحضير لـ MRCP و UKMLA\n\n"
        f"📌 خطتك الحالية: {plan}\n\n"
        "المتاح حاليًا:\n"
        "✅ التسجيل مجاني\n"
        "✅ النظام الأساسي جاهز\n\n"
        "قريبًا:\n"
        "📚 الحالات السريرية\n"
        "❓ MCQs\n"
        "📝 History Taking\n"
        "⭐ Premium Plan"
    )


# =========================
# استقبال الرسائل
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🩺 سيتم إضافة المحتوى الطبي والذكاء الاصطناعي قريبًا."
    )


# =========================
# تشغيل البوت
# =========================

def main():

    if not BOT_TOKEN:
        print("BOT_TOKEN غير موجود")
        return


    # إنشاء قاعدة البيانات عند التشغيل
    create_database()


    app = Application.builder().token(BOT_TOKEN).build()


    app.add_handler(
        CommandHandler("start", start)
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )


    print("MedMRCP AI Bot is running...")


    app.run_polling()



if __name__ == "__main__":
    main()
