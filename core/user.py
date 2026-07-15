import sqlite3

from core.database import DATABASE_NAME



# =========================
# الحصول على مستخدم
# =========================

def get_user_profile(user_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT user_id, username, first_name, plan, join_date
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )


    user = cursor.fetchone()

    conn.close()

    return user



# =========================
# معرفة خطة المستخدم
# =========================

def get_user_plan(user_id):

    user = get_user_profile(user_id)


    if user:
        return user[3]


    return "free"



# =========================
# ترقية المستخدم
# =========================

def upgrade_user(user_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users
        SET plan='premium'
        WHERE user_id=?
        """,
        (user_id,)
    )


    conn.commit()
    conn.close()



# =========================
# إرجاع المستخدم إلى Free
# =========================

def downgrade_user(user_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users
        SET plan='free'
        WHERE user_id=?
        """,
        (user_id,)
    )


    conn.commit()
    conn.close()



# =========================
# عدد المستخدمين
# (للوحة الإدارة لاحقًا)
# =========================

def count_users():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )


    count = cursor.fetchone()[0]


    conn.close()

    return count
