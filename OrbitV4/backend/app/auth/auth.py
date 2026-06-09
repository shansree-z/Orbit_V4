from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3
import hashlib
import base64

# Ensure database can be imported
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import get_db

SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Use plaintext context to avoid bcrypt issues
try:
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
except Exception:
    # Fallback: use simple hashing
    pwd_context = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password"""
    if pwd_context:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            pass
    # Fallback: simple hash comparison
    return hash_password_simple(plain_password) == hashed_password

def hash_password_simple(password: str) -> str:
    """Simple password hashing using PBKDF2"""
    import hashlib
    salt = "onboarding-concierge"
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return base64.b64encode(hash_obj).decode()

def get_password_hash(password: str) -> str:
    """Hash password"""
    if pwd_context:
        try:
            return pwd_context.hash(password)
        except Exception:
            pass
    # Fallback: simple hash
    return hash_password_simple(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate user against database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT email, password, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    db.close()
    
    if not user:
        return None
    
    if not verify_password(password, user[1]):
        return None
    
    return {
        "email": user[0],
        "role": user[2]
    }
