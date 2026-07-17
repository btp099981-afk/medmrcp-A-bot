import sqlite3
from datetime import datetime


DATABASE_NAME = "medmrcp.db"



# =========================
# Database Connection
# =========================

def get_connection():

    return sqlite3.connect(
        DATABASE_NAME
    )



# =========================
# Create Database
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
    CREATE TABLE IF NOT EXISTS payment_requests (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        proof TEXT,

        status TEXT DEFAULT 'pending',

        date TEXT

    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_agreements (

        user_id INTEGER PRIMARY KEY,

        disclaimer_accepted INTEGER DEFAULT 0,

        date TEXT

    )
    """)



    cursor.execute("""
    INSERT OR IGNORE INTO settings
    (key,value)

    VALUES
    ('premium_price','0')
    """)


    cursor.execute("""
    INSERT OR IGNORE INTO settings
    (key,value)

    VALUES
    ('payment_account','Not set')
    """)


    cursor.execute("""
    INSERT OR IGNORE INTO settings
    (key,value)

    VALUES
    ('whop_link','Not set')
    """)


    conn.commit()
    conn.close()



# =========================
# Users
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



def get_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM users

        WHERE user_id=?

        """,
        (user_id,)
    )


    user = cursor.fetchone()

    conn.close()

    return user



def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM users

        """
    )


    users = cursor.fetchall()

    conn.close()

    return users
    # =========================
# Phone
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

# =========================
# Payment Requests
# =========================

def create_payment_request(
    user_id,
    proof
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO payment_requests

        (
        user_id,
        proof,
        status,
        date
        )

        VALUES (?,?,?,?)

        """,
        (
            user_id,
            proof,
            "pending",
            datetime.now().strftime("%Y-%m-%d")
        )
    )


    conn.commit()
    conn.close()



def get_pending_payments():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *

        FROM payment_requests

        WHERE status='pending'

        """
    )


    requests = cursor.fetchall()

    conn.close()

    return requests



def update_payment_status(
    request_id,
    status
):

    conn = get_connection()
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



# =========================
# Admin Payment Actions
# =========================

def approve_payment(user_id):

    update_plan(
        user_id,
        "premium"
    )



def reject_payment(request_id):

    update_payment_status(
        request_id,
        "rejected"
    )



# =========================
# Database Test
# =========================

def test_database():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT name

        FROM sqlite_master

        WHERE type='table'
        """
    )


    tables = cursor.fetchall()


    conn.close()

    return tables
   
