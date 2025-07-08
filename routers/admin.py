from fastapi import APIRouter, Path, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from ..models import Users, Words
from ..database import SessionLocal
from .auth import get_current_user


router = APIRouter(prefix='/admin', tags=['admin'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/word', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    return db.query(Words).all()


@router.delete('/word/{word_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(user: user_dependency, db: db_dependency, word_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    word_model = db.query(Words).filter(Words.id == word_id).first()
    if word_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found!')
    
    db.query(Words).filter(Words.id == word_id).delete()
    db.commit()