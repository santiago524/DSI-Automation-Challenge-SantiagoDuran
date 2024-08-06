from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union



fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "hola",
        "disable": False,
    }
}

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer("/token")

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disable: Union[bool, None] = None

class UserInDB(User):
    hashed_password : str

def get_user(db, username):
    if username in db:
        user_data = db[username]
        return User(**user_data)
    return []

def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)


@app.get("/")
def root():
    return 'Hi there'

@app.get("/users/me")
def user(token: str = Depends(oauth2_scheme)):
    print(token)
    return 'i am user'

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    return {
        "access_token": "Tomatito",
        "token_type": "bearer"
    }