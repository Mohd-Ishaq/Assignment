from fastapi import Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError
from .models import Data_Table
from .database import get_db
from .env_validate import setting
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta


ALGORITHM = setting.ALGORITHM
SECRET_KEY = setting.SECRET_KEY
EXPIRE_MINUTES = setting.EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def Generate_Access_Token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token, credential_exception):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = token_data.get("id")
        if id == None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return id


def get_current(token=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials",
        headers={"www-AUTHENTICATE": "BEARER"},
    )
    id = verify_access_token(token, credential_exception)
    user = db.query(Data_Table).filter(Data_Table.id == id).first()
    return user
