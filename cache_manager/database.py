import os
import sqlite3

database_path = "cache/database.db"


def init_tables():
    if not os.path.exists(os.path.dirname(database_path)):
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create tables if they do not exist
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS urls
                   (
                       id  INTEGER PRIMARY KEY AUTOINCREMENT,
                       url TEXT UNIQUE
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS titles
                   (
                       id    INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT UNIQUE
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS files
                   (
                       url_id    INTEGER,
                       title_id  INTEGER,
                       file_path TEXT UNIQUE,
                       PRIMARY KEY (url_id, title_id),
                       FOREIGN KEY (url_id) REFERENCES urls (id),
                       FOREIGN KEY (title_id) REFERENCES titles (id)
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS quick_files
                   (
                       id        INTEGER PRIMARY KEY AUTOINCREMENT,
                       url_id    INTEGER,
                       file_path TEXT UNIQUE,
                       FOREIGN KEY (url_id) REFERENCES urls (id)
                   )

                   """)

    conn.commit()
    conn.close()


def check_url_and_title_in_db(url, title) -> bool:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    url_id: int = cursor.execute("SELECT id FROM urls WHERE url=?", (url,)).fetchone()[0]
    if not url_id:
        return False
    title_id: int = cursor.execute("SELECT id FROM titles WHERE title=?", (title,)).fetchone()[0]
    if not title_id:
        return False
    file_path: int = \
        cursor.execute("SELECT file_path FROM files WHERE url_id=? AND title_id=?", (url_id, title_id)).fetchone()[0]
    if not file_path:
        return False
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist, removing from database.")
        cursor.execute("DELETE FROM files WHERE url_id=? AND title_id=?", (url_id, title_id))
        conn.commit()
        conn.close()
        return False
    return True
