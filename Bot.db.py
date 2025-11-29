import sqlite3

conn = sqlite3.connect("test.db",check_same_thread=False) #Создает подключение к BD
cur = conn.cursor()# Создание терминала для ввода команды

cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT
)
""")
conn.commit()

def add_note(user_id,text):
    cur.execute("INSERT INTO notes (user_id,text) VALUES (?, ?)",(user_id,text))
    conn.commit()


def get_note(user_id):
    cur.execute("SELECT id,text FROM notes WHERE user_id = ?",(user_id,))
    return cur.fetchall()


def delete_note(note_id):
    cur.execute("DELETE FROM notes WHERE id = ?",(note_id,))
    conn.commit()

def edit_note(note_id,new_text):
    cur.execute("UPDATE notes SET text=? WHERE id=?", (note_id,new_text))
    conn.commit()
