from fastapi import APIRouter, Path, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
import traceback
from ..models import Words, CorrectIncorrect, Sentences
from ..schemas import WordUpdateRequest
from ..dependencies import db_dependency
from ..config import templates
from ..utils.auth_utils import redirect_to_login, get_current_user


router = APIRouter(prefix='/words', tags=['words'])


### Page ###

@router.get('/', response_class=HTMLResponse)
async def words_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        return templates.TemplateResponse('words.html', {
            "request": request,
            "user": user
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
async def create_word(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))
    data = await request.json()

    word_data = data.get('word', {})
    sentence_data = data.get('sentence', {})
    correct_data = data.get('correct_incorrect', {})

    word_text = word_data.get('word', '').strip()
    meaning = word_data.get('meaning', '').strip()
    sentence = sentence_data.get('sentence', '').strip()
    is_correct = correct_data.get('is_last_time_correct', False)

    if not word_text or not meaning or not sentence:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required.")

    # Check if word already exists for this user
    existing = db.query(Words).filter(
        Words.owner_id == user.get('id'),
        Words.word.ilike(word_text)
    ).first()

    if existing:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Word already exists."}
        )

    word_model = Words(
        word=word_text,
        meaning=meaning,
        owner_id=user.get('id')
    )
    db.add(word_model)
    db.commit()
    db.refresh(word_model)

    correct_model = CorrectIncorrect(
        word_id=word_model.id,
        owner_id=user.get('id'),
        is_last_time_correct=is_correct
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
