import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'tutormove.db'

conn = sqlite3.connect(DB_PATH)

# Initialize tables if they don't exist
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    verified_email INTEGER DEFAULT 0,
    verified_phone INTEGER DEFAULT 0,
    credits INTEGER DEFAULT 0
)''')

conn.execute('''
CREATE TABLE IF NOT EXISTS otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    code TEXT NOT NULL,
    purpose TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()

