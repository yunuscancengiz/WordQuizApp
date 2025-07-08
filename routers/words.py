from fastapi import APIRouter, Path, Query, HTTPException, Depends, Request, status
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from ..models import Words
from ..database import SessionLocal
from .auth import get_current_user




templates = Jinja2Templates(directory='WordQuizApp/templates')
router = APIRouter(prefix='/words', tags=['words'])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class WordRequest(BaseModel):
    word: str = Field(min_length=1, max_length=100)
    meaning: str = Field(min_length=1, max_length=100)


def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


### Pages ###




### Endpoints ###

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    return db.query(Words).filter(Words.owner_id == user.get('id')).all()


@router.get('/word/{word_id}', status_code=status.HTTP_200_OK)
async def read_word(user: user_dependency, db: db_dependency, word_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    word_model = db.query(Words).filter(Words.id == word_id).filter(Words.owner_id == user.get('id')).first()
    if word_model:
        return word_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found!')


@router.post('/word', status_code=status.HTTP_201_CREATED)
async def create_word(user: user_dependency, db: db_dependency, word_request: WordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    word_model = Words(**word_request.model_dump(), owner_id=user.get('id'))
    db.add(word_model)
    db.commit()


@router.put('/word/{word_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_word(user: user_dependency, db: db_dependency, word_request: WordRequest, word_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    word_model = db.query(Words).filter(Words.id == word_id).filter(Words.owner_id == user.get('id')).first()
    if word_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found!')
    
    word_model.word = word_request.word
    word_model.meaning = word_request.meaning

    db.add(word_model)
    db.commit()


@router.delete('/word/{word_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(user: user_dependency, db: db_dependency, word_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    word_model = db.query(Words).filter(Words.id == word_id).filter(Words.owner_id == user.get('id')).first()
    if word_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found!')
    db.query(Words).filter(Words.id == word_id).delete()
    db.commit()