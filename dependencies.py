from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from .utils.auth_utils import get_current_user
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]