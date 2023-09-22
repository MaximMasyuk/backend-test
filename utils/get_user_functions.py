from typing import Optional
from fastapi import HTTPException, Request
from jose import JWTError, jwt
from pydentic_model import TokenData

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def get_current_user(request: Request):
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")