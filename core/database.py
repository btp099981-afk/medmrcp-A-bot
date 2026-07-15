import sqlite3
from datetime import datetime


DATABASE_NAME = "medmrcp.db"


# =========================
# إنشاء قاعدة البيانات
# =========================

def create_database():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    # جدول المستخدمين
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        plan TEXT DEFAULT 'free',
        join_date TEXT
    )
    """)


    # جدول الإعدادات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)


    conn.commit()
    conn.close()



# =========================
# إضافة مستخدم
# =========================

def add_user(user_id, username, first_name):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute("""
    INSERT OR IGNORE INTO users
    (user_id, username, first_name, join_date)
    VALUES (?, ?, ?, ?)
    """,
    (
        user_id,
        username,
        first_name,
        datetime.now().strftime("%Y-%m-%d")
    ))


    conn.commit()
    conn.close()



# =========================
# جلب بيانات المستخدم
# =========================

def get_user(user_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user



# =========================
# تحديث خطة المستخدم
# =========================

def update_plan(user_id, plan):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE users
    SET plan=?
    WHERE user_id=?
    """,
    (plan, user_id))


    conn.commit()
    conn.close()
