from fastapi import HTTPException
from passlib.context import CryptContext
class PasswordValidator:
    min_length = 8

    @classmethod
    def validate(cls, password: str):
        if len(password) < cls.min_length:
            raise HTTPException(status_code=400, detail=f"Password must be at least {cls.min_length} characters long")
        if not any(char.isdigit() for char in password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")

class Hash:
    def __init__(self, rounds: int = 4):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

hash_helper = Hash()