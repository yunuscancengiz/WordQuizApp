from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from ..models import Users
from ..schemas import CreateUserRequest, Token
from ..dependencies import db_dependency
from ..utils.auth_utils import create_access_token, authenticate_user
from ..config import templates, bcrypt_context


router = APIRouter(prefix='/auth', tags=['auth'])


### Pages ###

@router.get('/login-page', name="login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/register-page', name="register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


### Endpoints ###  

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!')
    token = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(days=10))
    return {'access_token': token, 'token_type': 'bearer'}
