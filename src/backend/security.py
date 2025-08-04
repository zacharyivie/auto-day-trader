import secrets
import hashlib
import base64

def generate_salt(length: int = 32) -> str:
    """Generate a random salt for a user"""
    salt_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(salt_bytes).decode("utf-8")

def hash_password(password: str, salt: str) -> str:
    """Hash a password with a salt"""
    salt_bytes = base64.urlsafe_b64decode(salt.encode("utf-8"))
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        100_000
    )
    return base64.urlsafe_b64encode(password_hash).decode("utf-8")

def hash_and_salt(password: str) -> tuple[str, str]:
    """Generate a salt and hash a password"""
    salt = generate_salt()
    password_hash = hash_password(password, salt)
    return password_hash, salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    return hash_password(password, salt) == password_hash

def derive_encryption_key(password: str, salt: str, context: str = "AutoDayTrader_Encryption") -> str:
    salt_bytes = base64.urlsafe_b64decode(salt.encode("utf-8"))
    context_salt = salt_bytes + context.encode("utf-8")
    encryption_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode('utf-8'),
        context_salt,
        150_000,
        32
    )
    return base64.urlsafe_b64encode(encryption_key).decode("utf-8")

if __name__ == "__main__":
    salt = generate_salt()
    password_hash = hash_password("password", salt)