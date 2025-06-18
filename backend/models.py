from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    email: str
    phone: str
    password_hash: str
    role: str  # 'student' or 'tutor'
    verified_email: bool
    verified_phone: bool
    credits: int

