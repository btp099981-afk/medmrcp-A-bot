# =========================
# MedMRCP AI Settings
# =========================


BOT_NAME = "MedMRCP AI"


# =========================
# الخطط
# =========================

PLANS = {

    "free": {
        "name": "Free Plan",
        "daily_cases": 3,
        "daily_mcqs": 10,
        "advanced_evaluation": False
    },


    "premium": {
        "name": "Premium Plan",
        "daily_cases": "unlimited",
        "daily_mcqs": "unlimited",
        "advanced_evaluation": True
    }

}


# =========================
# الدول والأسعار
# (سيتم نقلها لاحقًا للوحة الإدارة)
# =========================

PRICES = {

    "SD": {
        "country": "Sudan",
        "currency": "SDG",
        "price": 0
    },


    "EG": {
        "country": "Egypt",
        "currency": "USD",
        "price": 4
    },


    "IN": {
        "country": "India",
        "currency": "USD",
        "price": 4
    },


    "PK": {
        "country": "Pakistan",
        "currency": "USD",
        "price": 4
    },


    "OTHER": {
        "country": "Other Countries",
        "currency": "USD",
        "price": 9.99
    },


    "UK": {
        "country": "United Kingdom",
        "currency": "USD",
        "price": 14.99
    }

}


# =========================
# طرق الدفع
# =========================

PAYMENT_METHODS = {

    "whop": {
        "enabled": True,
        "name": "Whop"
    },


    "sudan_bank": {
        "enabled": True,
        "bank_name": "Sudan Bank",
        "account_number": "CHANGE_ME"
    },


    "usdt": {
        "enabled": False,
        "network": ""
    }

}
