import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        hours REAL,
        attendance REAL,
        status TEXT
    )
''')
conn.commit()
conn.close()
