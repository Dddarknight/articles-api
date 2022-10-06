from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from api_server.tokens.models import TokenData
from api_server import users
from api_server.database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "3355bd9f366579e95098e3c240385377f3f3a36c663a20d5d83b8d070165f679"
ALGORITHM = "HS256"


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users.crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
