import sqlite3

# ================= DATABASE CONNECT =================
def connect_db():
    return sqlite3.connect("gym.db")

# ================= CREATE ALL TABLES =================
def create_tables():
    conn = connect_db()
    c = conn.cursor()

    # ================= TRAINERS TABLE =================
    c.execute("""
    CREATE TABLE IF NOT EXISTS trainers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        specialization TEXT,
        experience TEXT,
        salary TEXT
    )
    """)

    # ================= MEMBERS TABLE =================
    c.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        trainer_id INTEGER
    )
    """)

    # ================= ATTENDANCE TABLE =================
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trainer_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

# RUN TABLE CREATION
create_tables()