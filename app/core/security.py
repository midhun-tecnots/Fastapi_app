from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from fastapi import Depends
from jose import jwt

from app.core.config import settings
from app.db import models
from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


ALGORITHM = "HS256"




def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: int = Depends(oauth2_scheme),db_: Session = Depends(get_db)) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        user_id = int(user_id)
        if user_id is None:
            return None
        else:
            db_user = db_.query(models.User).filter(
            models.User.id == user_id
            ).first()

            if db_user is None:
                return None
            else:
                return user_id
    except jwt.JWTError:
        return None