from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
import traceback
from ..models import Sentences, QuizStreaks, Users, Themes
from ..schemas import SentenceAnswerRequest
from ..dependencies import db_dependency
from ..config import templates
from ..utils.db_utils import get_random_sentences
from ..utils.auth_utils import redirect_to_login, get_current_user
from ..utils.check_answer_utils import handle_answer_evaluation


router = APIRouter(prefix='/ros', tags=['ros'])


### Pages ###

@router.get('/', response_class=HTMLResponse)
async def ros_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))

        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()
        
        original_sentence, splitted_sentence = get_random_sentences(db=db, user_id=user.get('id'))
        if not original_sentence:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'No sentences found.'})
        
        streak = 0
        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get('id')).first()
        if streak_model:
            streak = streak_model.streak

        return templates.TemplateResponse('ros.html', {
                    'request': request,
                    'user': user,
                    'theme': theme_model,
                    'sentence': splitted_sentence,
                    'original_sentence': original_sentence,
                    'streak': streak
                }
            )
    except:
        print(traceback.format_exc())
        return redirect_to_login()
    

### Endpoints ###

@router.post('/check')
async def check_answer(request: Request, db: db_dependency, sentence_answer_request: SentenceAnswerRequest):
    user = await get_current_user(token=request.cookies.get('access_token'))

    sentence_model = db.query(Sentences).filter(
        Sentences.owner_id == user.get('id'),
        Sentences.sentence == sentence_answer_request.current_sentence
    ).first()

    if not sentence_model:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'result': 'not_found'})
    
    correct_sentence = sentence_model.sentence.casefold().strip().rstrip('.')
    user_response = " ".join(sentence_answer_request.user_answer.casefold().split())
    correct = " ".join(correct_sentence.split())
    is_correct = user_response == correct

    return handle_answer_evaluation(
        word_id=sentence_model.word_id,
        user_id=user.get('id'),
        is_correct=is_correct,
        correct_meaning=correct_sentence,
        db=db
    )



@router.get('/next')
async def get_next_sentence(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))
    
    original_sentence, splitted_sentence = get_random_sentences(db=db, user_id=user.get('id'))
    if not original_sentence:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'No sentences found.'})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "original_sentence": original_sentence,
            "splitted_sentence": splitted_sentence
        }
    )