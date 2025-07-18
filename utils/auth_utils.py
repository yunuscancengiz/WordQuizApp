from fastapi import HTTPException, Depends, status
from starlette.responses import RedirectResponse
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Users
from ..config import SECRET_KEY, ALGORITHM, oauth2_bearer, bcrypt_context


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing."
        )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!')
        return {'sub': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response
    

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encode = {'sub': username, 'id': user_id, 'role': role, 'exp': expires}
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)