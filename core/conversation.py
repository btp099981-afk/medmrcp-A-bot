patient_answers = {
    "age": "I am 55 years old.",
    "location": "The pain is in the center of my chest.",
    "onset": "It started 2 hours ago.",
    "character": "It feels like pressure.",
    "radiation": "The pain goes to my left arm.",
    "associated": "I have sweating and shortness of breath."
}


def get_patient_response(question):

    question = question.lower()

    if "age" in question or "old" in question:
        return patient_answers["age"]

    elif "where" in question or "location" in question:
        return patient_answers["location"]

    elif "when" in question or "start" in question:
        return patient_answers["onset"]

    elif "feel" in question or "character" in question:
        return patient_answers["character"]

    elif "spread" in question or "radiat" in question:
        return patient_answers["radiation"]

    elif "symptom" in question or "associated" in question or "other" in question:
        return patient_answers["associated"]

    else:
        return "Could you ask me another question?"
