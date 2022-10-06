from datetime import datetime, timedelta
from typing import Union

from jose import jwt


SECRET_KEY = "3355bd9f366579e95098e3c240385377f3f3a36c663a20d5d83b8d070165f679"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
