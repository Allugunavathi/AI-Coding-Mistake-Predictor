import sqlite3

DATABASE = "history.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code TEXT,

            prediction TEXT,

            score INTEGER,

            datetime TEXT

        )
    """)

    conn.commit()

    conn.close()


def save_history(code, prediction, score, datetime):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO history
        (code, prediction, score, datetime)

        VALUES (?, ?, ?, ?)
        """,

        (code, prediction, score, datetime)

    )

    conn.commit()

    conn.close()
def get_history():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, code, prediction, score, datetime
        FROM history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
