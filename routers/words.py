from fastapi import APIRouter, Path, HTTPException, status
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..models import Words, CorrectIncorrect, Sentences
from ..schemas import WordRequest, CorrectIncorrectRequest, SentenceRequest
from ..dependencies import db_dependency, user_dependency


router = APIRouter(prefix='/words', tags=['words'])


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
async def create_word(user: user_dependency, db: db_dependency,
                      word_request: WordRequest,
                      correct_incorrect_request: CorrectIncorrectRequest,
                      sentence_request: SentenceRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    word_model = Words(**word_request.model_dump(), owner_id=user.get('id'))
    db.add(word_model)
    db.commit()
    db.refresh(word_model)

    owner_id = word_model.owner_id
    word_id = word_model.id

    correct_incorrect_model = CorrectIncorrect(
        is_last_time_correct=correct_incorrect_request.is_last_time_correct,
        owner_id=owner_id,
        word_id=word_id
    )
    db.add(correct_incorrect_model)
    db.commit()
    db.refresh(correct_incorrect_model)

    sentence_model = Sentences(
        sentence=sentence_request.sentence,
        word_id=word_id,
        owner_id=owner_id
    )
    db.add(sentence_model)
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