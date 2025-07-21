from datetime import datetime, date
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi.responses import JSONResponse
from ..models import CorrectIncorrect, QuizStreaks, DailyStreaks


def handle_answer_evaluation(word_id: int, user_id: int, is_correct: bool, correct_meaning: str, db: Session):
    try:
        now = datetime.now(tz=ZoneInfo('Europe/Istanbul'))
        today = date.today()

        # QuizStreaks update
        try:
            streak_model = db.query(QuizStreaks).filter(
                QuizStreaks.owner_id == user_id
            ).one()
        except NoResultFound:
            streak_model = QuizStreaks(owner_id=user_id, streak=0, max_streak=0)
            db.add(streak_model)
            db.commit()
            db.refresh(streak_model)

        if is_correct:
            streak_model.streak += 1
            streak_model.max_streak = max(streak_model.streak, streak_model.max_streak)
        else:
            streak_model.streak = 0
        streak_model.question_count += 1
        db.commit()

        # CorrectIncorrect update
        correct_incorrect_model = db.query(CorrectIncorrect).filter(
            CorrectIncorrect.word_id == word_id,
            CorrectIncorrect.owner_id == user_id
        ).first()

        if correct_incorrect_model:
            correct_incorrect_model.is_last_time_correct = is_correct
            correct_incorrect_model.last_attempted_at = now
            if is_correct:
                correct_incorrect_model.correct_count += 1
            else:
                correct_incorrect_model.incorrect_count += 1
        else:
            correct_incorrect_model = CorrectIncorrect(
                word_id=word_id,
                owner_id=user_id,
                is_last_time_correct=is_correct,
                correct_count=1 if is_correct else 0,
                incorrect_count=0 if is_correct else 1,
                last_attempted_at=now
            )
            db.add(correct_incorrect_model)

        # DailyStreaks update (always update today's record)
        today_record = db.query(DailyStreaks).filter(
            DailyStreaks.owner_id == user_id,
            DailyStreaks.date == today
        ).first()

        if today_record:
            today_record.max_streak = streak_model.max_streak
            today_record.question_count = streak_model.question_count
        else:
            today_record = DailyStreaks(
                owner_id=user_id,
                date=today,
                max_streak=streak_model.max_streak,
                question_count=streak_model.question_count
            )
            db.add(today_record)

        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "result": "correct" if is_correct else "incorrect",
                "correct_answer": correct_meaning,
                "streak": streak_model.streak,
                "max_streak": streak_model.max_streak
            }
        )

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to handle answer evaluation: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})
