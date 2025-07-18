from fastapi import HTTPException, Depends, status
from typing import Annotated
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import SessionLocal
from .config import SECRET_KEY, ALGORITHM, oauth2_bearer
from .models import Users
from .utils.auth_utils import get_current_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]