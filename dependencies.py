from fastapi import Depends
from fastapi.templating import Jinja2Templates
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from pathlib import Path
from .routers.auth import get_current_user, get_db


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))