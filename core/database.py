import sqlite3
from datetime import datetime


DATABASE_NAME = "medmrcp.db"



# =========================
# إنشاء قاعدة البيانات
# =========================

def create_database():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()



    # جدول المستخدمين

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY,

        username TEXT,

        first_name TEXT,

        phone_number TEXT,

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



    # جدول الخصومات

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discounts (

        user_id INTEGER PRIMARY KEY,

        discount_percent INTEGER DEFAULT 0

    )
    """)



    # جدول الدفع

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        status TEXT DEFAULT 'pending',

        date TEXT

    )
    """)



    # إعدادات افتراضية

    cursor.execute(
        """
        INSERT OR IGNORE INTO settings
        (key,value)

        VALUES
        ('premium_price','0')
        """
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO settings
        (key,value)

        VALUES
        ('payment_account','Not set')
        """
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO settings
        (key,value)

        VALUES
        ('whop_link','Not set')
        """
    )



    conn.commit()

    conn.close()




# =========================
# إضافة مستخدم
# =========================

def add_user(
    user_id,
    username,
    first_name
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()



    cursor.execute(
        """

        INSERT OR IGNORE INTO users

        (
        user_id,
        username,
        first_name,
        join_date
        )

        VALUES (?, ?, ?, ?)

        """,

        (

        user_id,

        username,

        first_name,

        datetime.now().strftime(
            "%Y-%m-%d"
        )

        )

    )



    conn.commit()

    conn.close()




# =========================
# تحديث رقم الهاتف
# =========================

def update_phone(
    user_id,
    phone
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users

        SET phone_number=?

        WHERE user_id=?

        """,

        (
            phone,
            user_id
        )

    )


    conn.commit()

    conn.close()




# =========================
# جلب بيانات المستخدم
# =========================

def get_user(
    user_id
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM users

        WHERE user_id=?

        """,

        (
            user_id,
        )

    )


    user = cursor.fetchone()


    conn.close()


    return user




# =========================
# البحث برقم الهاتف
# =========================

def get_user_by_phone(
    phone
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM users

        WHERE phone_number=?

        """,

        (
            phone,
        )

    )


    user = cursor.fetchone()


    conn.close()


    return user




# =========================
# تحديث الخطة
# =========================

def update_plan(
    user_id,
    plan
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        UPDATE users

        SET plan=?

        WHERE user_id=?

        """,

        (
            plan,
            user_id
        )

    )


    conn.commit()

    conn.close()




# =========================
# إضافة خصم
# =========================

def add_discount(
    user_id,
    percent
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        INSERT OR REPLACE INTO discounts

        (
        user_id,
        discount_percent
        )

        VALUES (?,?)

        """,

        (
            user_id,
            percent
        )

    )


    conn.commit()

    conn.close()




# =========================
# جلب الخصم
# =========================

def get_discount(
    user_id
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        SELECT discount_percent

        FROM discounts

        WHERE user_id=?

        """,

        (
            user_id,
        )

    )


    result = cursor.fetchone()


    conn.close()


    if result:

        return result[0]


    return 0




# =========================
# تغيير إعداد
# =========================

def update_setting(
    key,
    value
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        INSERT OR REPLACE INTO settings

        (
        key,
        value
        )

        VALUES (?,?)

        """,

        (
            key,
            value
        )

    )


    conn.commit()

    conn.close()




# =========================
# جلب إعداد
# =========================

def get_setting(
    key
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        SELECT value

        FROM settings

        WHERE key=?

        """,

        (
            key,
        )

    )


    result = cursor.fetchone()


    conn.close()


    if result:

        return result[0]


    return None
