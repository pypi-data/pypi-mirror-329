# syntaxmatrix/db.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "syntaxmatrix.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            name TEXT PRIMARY KEY,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_pages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM pages")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def add_page(name, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pages (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    conn.close()

def update_page(old_name, new_name, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE pages SET name = ?, content = ? WHERE name = ?", (new_name, content, old_name))
    conn.commit()
    conn.close()

def delete_page(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pages WHERE name = ?", (name,))
    conn.commit()
    conn.close()
