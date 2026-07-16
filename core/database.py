import sqlite3
from datetime import datetime


DATABASE_NAME = "medmrcp.db"



# =========================
# الاتصال
# =========================

def get_connection():

    return sqlite3.connect(
        DATABASE_NAME
    )



# =========================
# إنشاء قاعدة البيانات
# =========================

def create_database():

    conn = get_connection()

    cursor = conn.cursor()


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


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        key TEXT PRIMARY KEY,

        value TEXT

    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discounts (

        user_id INTEGER PRIMARY KEY,

        discount_percent INTEGER DEFAULT 0

    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        status TEXT,

        date TEXT

    )
    """)


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

    conn = get_connection()

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

        VALUES (?,?,?,?)

        """,
        (
            user_id,
            username,
            first_name,
            datetime.now().strftime("%Y-%m-%d")
        )
    )


    conn.commit()
    conn.close()



# =========================
# جلب مستخدم
# =========================

def get_user(user_id):

    conn = get_connection()

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
# البحث بالهاتف
# =========================

def get_user_by_phone(phone):

    conn = get_connection()

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
# تحديث الهاتف
# =========================

def update_phone(
    user_id,
    phone
):

    conn = get_connection()

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
# تحديث الخطة
# =========================

def update_plan(
    user_id,
    plan
):

    conn = get_connection()

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
# الخصومات
# =========================

def add_discount(
    user_id,
    percent
):

    conn = get_connection()

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



def get_discount(user_id):

    conn = get_connection()

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
# الإعدادات
# =========================

def update_setting(
    key,
    value
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR REPLACE INTO settings

        (key,value)

        VALUES (?,?)
        """,
        (
            key,
            value
        )
    )


    conn.commit()
    conn.close()



def get_setting(key):

    conn = get_connection()

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
# =========================
# إنشاء طلب دفع
# =========================

def create_payment_request(
    user_id,
    proof
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO payment_requests
        (
        user_id,
        proof,
        date
        )

        VALUES (?, ?, ?)
        """,

        (
            user_id,
            proof,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )

    )


    conn.commit()

    conn.close()
# =========================
# جلب طلبات الدفع المعلقة
# =========================

def get_pending_payments():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM payment_requests

        WHERE status='pending'
        """
    )


    data = cursor.fetchall()


    conn.close()


    return data
# =========================
# تحديث حالة الدفع
# =========================

def update_payment_status(
    request_id,
    status
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE payment_requests

        SET status=?

        WHERE id=?

        """,

        (
            status,
            request_id
        )

    )


    conn.commit()

    conn.close()
