from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
import traceback
from models import Words, QuizStreaks, Users, Themes
from schemas import AnswerRequest
from dependencies import db_dependency
from config import templates
from utils.db_utils import get_random_quiz_word_and_choices
from utils.auth_utils import redirect_to_login, get_current_user
from utils.check_answer_utils import handle_answer_evaluation
from utils.streak_utils import update_daily_streak_if_needed


router = APIRouter(prefix='/quiz', tags=['quiz'])


### Pages ###

@router.get('/', response_class=HTMLResponse)
async def quiz_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))

        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()

        word, choices = get_random_quiz_word_and_choices(db=db, user_id=user.get('id'))
        if not word or not choices:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'No quiz data found.'})

        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get('id')).first()
        streak = streak_model.streak if streak_model else 0

        return templates.TemplateResponse('quiz.html', {
            'request': request,
            'user': user,
            'theme': theme_model,
            'word': word,
            'choices': choices,
            'streak': streak
        })
    except:
        print(traceback.format_exc())
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

    update_daily_streak_if_needed(db=db, user_id=user.get('id'))
    return handle_answer_evaluation(
        word_id=word_model.id,
        user_id=user.get('id'),
        is_correct=is_correct,
        correct_meaning=correct_meaning,
        db=db
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
