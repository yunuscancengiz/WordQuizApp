from datetime import datetime
from zoneinfo import ZoneInfo
from ..models import DailyStreaks, QuizStreaks


def update_daily_streak_if_needed(db, user_id):
    today = datetime.now(tz=ZoneInfo("Europe/Istanbul")).date()

    latest_entry = (
        db.query(DailyStreaks)
        .filter(DailyStreaks.owner_id == user_id)
        .order_by(DailyStreaks.date.desc())
        .first()
    )

    if latest_entry and latest_entry.date == today:
        return  
    
    streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user_id).first()
    if not streak_model:
        return

    if latest_entry and latest_entry.date < today:
        latest_entry.max_streak = streak_model.max_streak
        latest_entry.question_count = streak_model.question_count

    new_streak = DailyStreaks(
        date=today,
        max_streak=0,
        question_count=0,
        owner_id=user_id
    )
    db.add(new_streak)

    streak_model.streak = 0
    streak_model.max_streak = 0
    streak_model.question_count = 0

    db.commit()
