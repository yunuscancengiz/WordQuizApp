from fastapi import APIRouter, HTTPException, status
from models import Users
from schemas import UserVerification
from dependencies import db_dependency, user_dependency
from config import bcrypt_context


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.post('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong Password!')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()