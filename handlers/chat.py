from core.conversation import get_patient_response


async def handle_message(update, context):

    user_question = update.message.text

    response = get_patient_response(user_question)

    await update.message.reply_text(response)
