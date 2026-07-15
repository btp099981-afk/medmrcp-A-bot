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

# تحميل إعدادات البيئة
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================
# أمر البداية /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"👋 أهلاً بك {user.first_name} في MedMRCP AI\n\n"
        "🩺 مساعدك الذكي للتحضير لـ MRCP و UKMLA.\n\n"
        "المميزات القادمة:\n"
        "✅ حالات سريرية\n"
        "✅ MCQs\n"
        "✅ History Taking\n"
        "✅ تقييم مستوى الطالب\n\n"
        "سيتم تجهيز النظام الكامل قريباً."
    )


# =========================
# استقبال الرسائل
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    await update.message.reply_text(
        "تم استلام رسالتك ✅\n\n"
        f"رسالتك: {text}\n\n"
        "سيتم ربط الذكاء الاصطناعي والمحتوى الطبي في المراحل القادمة."
    )


# =========================
# تشغيل البوت
# =========================

def main():

    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN غير موجود")
        return

    app = Application.builder().token(BOT_TOKEN).build()


    # أمر البداية
    app.add_handler(
        CommandHandler("start", start)
    )


    # الرسائل النصية
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
