import hashlib
import os
import sqlite3
from .database import conn


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + pwd_hash.hex()


def register_user(username: str, email: str, phone: str, password: str, role: str) -> int:
    password_hash = _hash_password(password)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (username, email, phone, password_hash, role) VALUES (?, ?, ?, ?, ?)',
        (username, email, phone, password_hash, role)
    )
    conn.commit()
    return cur.lastrowid


def create_otp(user_id: int, purpose: str) -> str:
    code = str(os.urandom(3).hex())
    conn.execute(
        'INSERT INTO otps (user_id, code, purpose) VALUES (?, ?, ?)',
        (user_id, code, purpose)
    )
    conn.commit()
    return code


def verify_otp(user_id: int, code: str, purpose: str) -> bool:
    cur = conn.execute(
        'SELECT id FROM otps WHERE user_id = ? AND code = ? AND purpose = ? ORDER BY created_at DESC LIMIT 1',
        (user_id, code, purpose)
    )
    row = cur.fetchone()
    if not row:
        return False
    if purpose == 'email':
        conn.execute('UPDATE users SET verified_email=1 WHERE id=?', (user_id,))
    elif purpose == 'phone':
        conn.execute('UPDATE users SET verified_phone=1 WHERE id=?', (user_id,))
    conn.commit()
    return True


def authenticate(username: str, password: str) -> bool:
    cur = conn.execute('SELECT password_hash FROM users WHERE username=?', (username,))
    row = cur.fetchone()
    if not row:
        return False
    stored = row[0]
    salt = bytes.fromhex(stored[:32])
    stored_hash = stored[32:]
    test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    return stored_hash == test_hash

