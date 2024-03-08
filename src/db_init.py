import sqlite3


def init_db():
    conn = sqlite3.connect("sqlite3.db")
    conn.execute("CREATE TABLE members (user_id TEXT)")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
