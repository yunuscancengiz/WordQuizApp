from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import func, desc
from datetime import date, timedelta
import traceback
from models import Users, Themes, DailyStreaks, QuizStreaks, CorrectIncorrect, Words
from dependencies import db_dependency
from config import templates
from utils.auth_utils import redirect_to_login, get_current_user


router = APIRouter(prefix='/dashboard', tags=['dashboard'])


@router.get('/', response_class=HTMLResponse)
async def dashboard_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))

        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()

        ### Daily Streaks (line chart)
        today = date.today()
        start_date = today - timedelta(days=30)

        daily_streaks = (
            db.query(DailyStreaks)
            .filter(
                DailyStreaks.owner_id == user_model.id,
                DailyStreaks.date >= start_date
            )
            .order_by(DailyStreaks.date.asc())
            .all()
        )

        daily_streaks_dates = [ds.date.isoformat() for ds in daily_streaks]
        daily_streaks_max = [ds.max_streak for ds in daily_streaks]
        daily_streaks_question_count = [ds.question_count for ds in daily_streaks]

        ### Accuracy (doughnut chart)
        correct_data = db.query(CorrectIncorrect).filter_by(owner_id=user_model.id).all()
        correct_total = sum(ci.correct_count for ci in correct_data)
        incorrect_total = sum(ci.incorrect_count for ci in correct_data)

        ### Quiz Stats (bar chart)
        quiz_model = db.query(QuizStreaks).filter_by(owner_id=user_model.id).first()
        quiz_max_streak = quiz_model.max_streak if quiz_model else 0
        quiz_question_count = quiz_model.question_count if quiz_model else 0

        ### Most Incorrect Words (stacked bar)
        top5_incorrect = (
            db.query(CorrectIncorrect, Words)
            .join(Words, Words.id == CorrectIncorrect.word_id)
            .filter(CorrectIncorrect.owner_id == user_model.id)
            .order_by(desc(CorrectIncorrect.incorrect_count))
            .limit(5)
            .all()
        )
        hardest_words_labels = [word.word for _, word in top5_incorrect]
        hardest_words_incorrect = [ci.incorrect_count for ci, _ in top5_incorrect]
        hardest_words_correct = [ci.correct_count for ci, _ in top5_incorrect]

        ### Most Correct Words (bar)
        top5_correct = (
            db.query(CorrectIncorrect, Words)
            .join(Words, Words.id == CorrectIncorrect.word_id)
            .filter(CorrectIncorrect.owner_id == user_model.id)
            .order_by(desc(CorrectIncorrect.correct_count))
            .limit(5)
            .all()
        )
        most_correct_words_labels = [word.word for _, word in top5_correct]
        most_correct_words_data = [ci.correct_count for ci, _ in top5_correct]

        return templates.TemplateResponse('dashboard.html', {
            'request': request,
            'user': user,
            'theme': theme_model,
            'dashboard_data': {
                'daily_streaks_dates': daily_streaks_dates,
                'daily_streaks_max': daily_streaks_max,
                'daily_streaks_question_count': daily_streaks_question_count,
                'correct_total': correct_total,
                'incorrect_total': incorrect_total,
                'quiz_max_streak': quiz_max_streak,
                'quiz_question_count': quiz_question_count,
                'hardest_words_labels': hardest_words_labels,
                'hardest_words_incorrect': hardest_words_incorrect,
                'hardest_words_correct': hardest_words_correct,
                'most_correct_words_labels': most_correct_words_labels,
                'most_correct_words_data': most_correct_words_data,
            }
        })

    except Exception as e:
        print(traceback.format_exc())
        return redirect_to_login()