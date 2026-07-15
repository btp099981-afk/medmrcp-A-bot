from core.users import get_user_plan
from core.settings import PLANS



# =========================
# التحقق من خطة المستخدم
# =========================

def is_premium(user_id):

    plan = get_user_plan(user_id)

    return plan == "premium"



# =========================
# حدود الحالات اليومية
# =========================

def get_daily_case_limit(user_id):

    plan = get_user_plan(user_id)


    if plan in PLANS:

        return PLANS[plan]["daily_cases"]


    return PLANS["free"]["daily_cases"]



# =========================
# حدود MCQs اليومية
# =========================

def get_daily_mcq_limit(user_id):

    plan = get_user_plan(user_id)


    if plan in PLANS:

        return PLANS[plan]["daily_mcqs"]


    return PLANS["free"]["daily_mcqs"]



# =========================
# الميزات المتقدمة
# =========================

def has_advanced_features(user_id):

    plan = get_user_plan(user_id)


    if plan in PLANS:

        return PLANS[plan]["advanced_evaluation"]


    return False



# =========================
# رسالة الخطة
# =========================

def subscription_info(user_id):

    plan = get_user_plan(user_id)


    if plan == "premium":

        return (
            "⭐ Premium Plan\n\n"
            "✅ حالات غير محدودة\n"
            "✅ MCQs غير محدودة\n"
            "✅ History Taking\n"
            "✅ تقييم متقدم"
        )


    return (
        "🆓 Free Plan\n\n"
        "✅ حالات محدودة يوميًا\n"
        "✅ MCQs محدودة\n"
        "✅ تقييم أساسي\n\n"
        "يمكنك الترقية إلى Premium لاحقًا."
    )
