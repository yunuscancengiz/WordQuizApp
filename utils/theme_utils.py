from dependencies import db_dependency
from models import Users, Themes



def get_theme_by_id(db: db_dependency, theme_id: int) -> Themes:
    theme = db.query(Themes).filter(Themes.id == theme_id).first()
    if theme:
        return theme
    return db.query(Themes).filter(Themes.is_default == True).first()