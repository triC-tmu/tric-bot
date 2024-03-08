import sqlite3


def get_members():
    conn = sqlite3.connect("sqlite3.db")
    cursor = conn.execute("SELECT user_id FROM members")
    members = []
    for row in cursor:
        members.append(row[0])
    conn.close()
    return members


def add_member(user_id):
    conn = sqlite3.connect("sqlite3.db")
    conn.execute(f"INSERT INTO members (user_id) VALUES ('{user_id}')")
    conn.commit()
    conn.close()
