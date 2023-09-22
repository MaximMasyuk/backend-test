from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydentic_model import UserResponse, TokenData
from services.auth import login_post, registration_post, get_user
from utils.get_user_functions import get_current_user


app = APIRouter()


@app.post("/sign_up")
def register(username: str, email: str, surname: str, password: str):
    sisignature, user_id = registration_post(username, email, surname, password)
    return {"user_id": user_id, "signature": sisignature}


@app.post("/sign_in")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = login_post(form_data)
    return {"access_token": access_token}


@app.get("/user", response_model=UserResponse)
def read_users_me(token_data: TokenData = Depends(get_current_user)):
    user_response = get_user(token_data)
    return user_response
