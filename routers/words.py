from fastapi import APIRouter, Path, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
import traceback
from models import Words, CorrectIncorrect, Sentences, Users, Themes
from schemas import WordUpdateRequest, CreateWordRequest
from dependencies import db_dependency
from config import templates
from utils.auth_utils import redirect_to_login, get_current_user


router = APIRouter(prefix='/words', tags=['words'])


### Page ###

@router.get('/', response_class=HTMLResponse)
async def words_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))

        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()

        return templates.TemplateResponse('words.html', {
            'request': request,
            'user': user,
            'theme': theme_model
        })
    except:
        print(traceback.format_exc())
        return redirect_to_login()


### Endpoints ###

@router.get('/api', status_code=status.HTTP_200_OK)
async def read_all(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))
    return db.query(Words).filter(Words.owner_id == user.get('id')).all()


@router.get('/word/{word_id}', status_code=status.HTTP_200_OK)
async def read_word(request: Request, db: db_dependency, word_id: int = Path(ge=0)):
    user = await get_current_user(token=request.cookies.get('access_token'))

    word_model = db.query(Words).filter(
        Words.id == word_id,
        Words.owner_id == user.get('id')
    ).first()

    if not word_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found!')

    sentence_model = db.query(Sentences).filter(
        Sentences.word_id == word_id,
        Sentences.owner_id == user.get('id')
    ).first()

    return {
        "id": word_model.id,
        "word": word_model.word,
        "meaning": word_model.meaning,
        "sentence": sentence_model.sentence if sentence_model else None
    }


@router.post('/word', status_code=status.HTTP_201_CREATED)
async def create_word(request: Request, db: db_dependency, create_word_request: CreateWordRequest):
    user = await get_current_user(token=request.cookies.get('access_token'))

    word = create_word_request.word
    meaning = create_word_request.translition
    sentence = create_word_request.example_sentence

    if not word or not meaning or not sentence:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required.")

    # Check if word already exists for this user
    existing = db.query(Words).filter(
        Words.owner_id == user.get('id'),
        Words.word.ilike(word)
    ).first()

    if existing:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Word already exists."}
        )

    word_model = Words(
        word=word,
        meaning=meaning,
        owner_id=user.get('id')
    )
    db.add(word_model)
    db.commit()
    db.refresh(word_model)

    correct_model = CorrectIncorrect(
        word_id=word_model.id,
        owner_id=user.get('id'),
        is_last_time_correct=False
    )
    db.add(correct_model)

    sentence_model = Sentences(
        word_id=word_model.id,
        owner_id=user.get('id'),
        sentence=sentence
    )
    db.add(sentence_model)
    db.commit()

    return {"message": "Word created successfully."}


@router.post('/bulk-create')
async def bulk_create_words(request: Request, db: db_dependency, word_list: List[CreateWordRequest]):
    user = await get_current_user(token=request.cookies.get('access_token'))

    if user['user_role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can bulk create words.')
    
    created = []
    skipped = []

    for word_data in word_list:
        existing = db.query(Words).filter(
            Words.word.ilike(word_data.word)
        ).first()

        if existing:
            skipped.append(word_data.word)
            continue

        word_model = Words(
            word=word_data.word,
            meaning=word_data.translition,
            owner_id=user.get('id')
        )
        db.add(word_model)
        db.commit()
        db.refresh(word_model)

        correct_incorrect_model = CorrectIncorrect(
            word_id=word_model.id,
            owner_id=user.get('id'),
            is_last_time_correct=False
        )
        db.add(correct_incorrect_model)

        sentence_model = Sentences(
            sentence=word_data.example_sentence,
            word_id=word_model.id,
            owner_id=user.get('id')
        )
        db.add(sentence_model)
        created.append(word_data.word)
    db.commit()
    
    return {
        'message': 'Words processed.',
        'created': created,
        'skipped': skipped
    }


@router.put('/word/{word_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_word(
    request: Request,
    db: db_dependency,
    word_id: int = Path(ge=0),
    word_request: WordUpdateRequest = None
):
    user = await get_current_user(token=request.cookies.get('access_token'))

    # Verileri al
    word_text = word_request.word.strip()
    meaning = word_request.meaning.strip()
    sentence = word_request.sentence.strip()

    if not word_text or not meaning or not sentence:
        raise HTTPException(status_code=400, detail="All fields are required.")

    # Word tablosu
    word_model = db.query(Words).filter(
        Words.id == word_id,
        Words.owner_id == user.get('id')
    ).first()

    if not word_model:
        raise HTTPException(status_code=404, detail="Word not found!")

    word_model.word = word_text
    word_model.meaning = meaning

    # Sentence tablosu
    sentence_model = db.query(Sentences).filter(
        Sentences.word_id == word_id,
        Sentences.owner_id == user.get('id')
    ).first()

    if sentence_model:
        sentence_model.sentence = sentence
    else:
        db.add(Sentences(
            word_id=word_id,
            owner_id=user.get('id'),
            sentence=sentence
        ))

    db.commit()


@router.delete('/delete-all')
async def delete_all_songs(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))

    if user['user_role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admins can delete all songs.'
        )

    deleted_count = db.query(Words).delete()
    db.query(CorrectIncorrect).delete()
    db.query(Sentences).delete()
    db.commit()

    return {
        'message': f'{deleted_count} words and their related sentences deleted successfully.'
    }



@router.delete('/word/{word_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(request: Request, db: db_dependency, word_id: int = Path(ge=0)):
    user = await get_current_user(token=request.cookies.get('access_token'))

    word_model = db.query(Words).filter(
        Words.id == word_id,
        Words.owner_id == user.get('id')
    ).first()

    if word_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found!')

    db.query(Sentences).filter(
        Sentences.word_id == word_id,
        Sentences.owner_id == user.get('id')
    ).delete()

    db.query(CorrectIncorrect).filter(
        CorrectIncorrect.word_id == word_id,
        CorrectIncorrect.owner_id == user.get('id')
    ).delete()

    db.delete(word_model)
    db.commit()
