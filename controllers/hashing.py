"""Module for hashing and verifying passwords."""
from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str) -> str:
    """Return a hash of the password."""
    return pwd_ctx.hash(password)


def verify(hashed_string: str, plaintext_password: str) -> bool:
    """Check whether the given plaintext password equals the hashed string."""
    return pwd_ctx.verify(plaintext_password, hashed_string)
