from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.db_connection import SessionLocal
from models.models import UserDB

from pydentic_model import TokenData, UserResponse

from sqlalchemy import update

from utils.get_user_functions import get_current_user
from utils.login_function import create_access_token
from utils.registration_function import PasswordValidator, hash_helper
from utils.web3_transformation import transfer_to_keccak256, transfer_to_signed_message, signing_private_key

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def registration_post(username: str, email: str, surname: str, password: str):
    PasswordValidator.validate(password)
    hashed_password = hash_helper.get_password_hash(password)
    db = SessionLocal()
    user = UserDB(username=username, surname=surname, email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    result = db.query(UserDB.id).filter(UserDB.username == username).first()
    if result:
        user_id = result[0]
        hash_hax = transfer_to_keccak256(user_id)
        message = transfer_to_signed_message(hash_hax)
        sisignature = signing_private_key(message)
        update_query = update(UserDB).where(UserDB.id == user_id)
        update_query = update_query.values(eth_address=message, signature=sisignature)
        db.execute(update_query)
        db.commit()
    db.close()
    return sisignature, user_id


def login_post(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not hash_helper.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return access_token


def get_user(token_data: TokenData = Depends(get_current_user)):
    db = SessionLocal()
    user: UserDB = db.query(UserDB).filter(UserDB.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_response = UserResponse(id=str(user.id), username=user.username, surname=user.surname, email=user.email,
                                 eth_address=user.eth_address)
    return user_response
