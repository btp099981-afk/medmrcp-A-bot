import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler



# =========================
# قائمة نوع المحتوى
# =========================

def get_content_menu(system):

    keyboard = [

        [
            InlineKeyboardButton(
                "📖 Notes",
                callback_data=f"notes_{system}"
            )
        ],

        [
            InlineKeyboardButton(
                "🩺 Clinical Cases",
                callback_data=f"cases_{system}"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 MCQ Practice",
                callback_data=f"mcq_{system}"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back_menu"
            )
        ]

    ]


    return InlineKeyboardMarkup(keyboard)



# =========================
# تحديد اسم الملف
# =========================

def get_file_name(content_type, system):


    files = {

        "notes_cardiology":
        "cardiology_notes.txt",

        "notes_respiratory":
        "respiratory_notes.txt",

        "notes_neurology":
        "neurology_notes.txt",

        "notes_gastro":
        "gastro_notes.txt",

        "notes_renal":
        "renal_notes.txt",



        "cases_cardiology":
        "case_cardiology.txt",

        "cases_respiratory":
        "case_respiratory.txt",

        "cases_neurology":
        "case_neurology.txt",

        "cases_gastro":
        "case_gastro.txt",

        "cases_renal":
        "case_renal.txt"

    }


    return files.get(
        f"{content_type}_{system}"
    )



# =========================
# قراءة الملف
# =========================

def read_content(filename):

    if not filename:

        return "⚠️ Content not available yet."



    path = os.path.join(
        "content",
        filename
    )


    if not os.path.exists(path):

        return "⚠️ Content file not found."



    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# =========================
# فتح المحتوى
# =========================

async def open_content(update, context):

    query = update.callback_query

    await query.answer()


    data = query.data.split("_")


    content_type = data[0]

    system = data[1]



    filename = get_file_name(
        content_type,
        system
    )



    text = read_content(
        filename
    )



    await query.edit_message_text(
        text
    )



# =========================
# Handler
# =========================

def get_content_handler():

    return CallbackQueryHandler(

        open_content,

        pattern="^(notes|cases|mcq)_"

    )
