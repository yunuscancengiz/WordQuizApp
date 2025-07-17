from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.exc import NoResultFound
from ..models import Words, QuizStreaks
from ..schemas import AnswerRequest
from ..dependencies import db_dependency
from ..config import templates
from ..utils.db_utils import get_random_quiz_word_and_choices
from ..utils.auth_utils import get_current_user, redirect_to_login


router = APIRouter(prefix='/quiz', tags=['quiz'])


### Pages ###

@router.get('/', response_class=HTMLResponse)
async def quiz_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        word, choices = get_random_quiz_word_and_choices(db=db, user_id=user.get('id'))
        print(word, choices)
        if not word or not choices:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'No quiz data found.'})

        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get('id')).first()
        streak = streak_model.streak if streak_model else 0

        return templates.TemplateResponse('quiz.html', {
            'request': request,
            'user': user,
            'word': word,
            'choices': choices,
            'streak': streak
        })
    except:
        return redirect_to_login()


### Endpoints ###

@router.post('/check')
async def check_quiz_answer(request: Request, db: db_dependency, answer_request: AnswerRequest):
    user = await get_current_user(token=request.cookies.get('access_token'))

    word_model = db.query(Words).filter(
        Words.owner_id == user.get('id'),
        Words.word == answer_request.current_word
    ).first()

    if not word_model:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'result': 'not_found'})

    correct_meaning = word_model.meaning.casefold().strip()
    user_answer = answer_request.user_answer.casefold().strip()
    is_correct = correct_meaning == user_answer

    try:
        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get('id')).one()
    except NoResultFound:
        streak_model = QuizStreaks(owner_id=user.get('id'), streak=0, max_streak=0)
        db.add(streak_model)
        db.commit()
        db.refresh(streak_model)

    if is_correct:
        streak_model.streak += 1
        streak_model.max_streak = max(streak_model.streak, streak_model.max_streak)
    else:
        streak_model.streak = 0
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'result': 'correct' if is_correct else 'incorrect',
            'correct_answer': correct_meaning,
            'streak': streak_model.streak,
            'max_streak': streak_model.max_streak
        }
    )


@router.get('/next')
async def get_next_quiz(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))

    word, choices = get_random_quiz_word_and_choices(db=db, user_id=user.get('id'))
    if not word or not choices:
        return JSONResponse(status_code=404, content={'error': 'No quiz data found.'})

    streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get('id')).first()
    streak = streak_model.streak if streak_model else 0

    return JSONResponse(
        status_code=200,
        content={
            "word": word,
            "choices": choices,
            "streak": streak
        }
    )
