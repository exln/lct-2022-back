from datetime import timedelta
import hashlib
from random import randbytes
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from pydantic import EmailStr

import oauth2
import schemas
import models
import utilities
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import AuthJWT
from config import settings


router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.CreateUserSchema, request: Request, db: Session = Depends(get_db)):

    user_query = db.query(models.User)
    user = user_query.first()

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')

    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

    payload.password = utilities.hash_password(payload.password)
    del payload.passwordConfirm

    payload.role = 'user'
    payload.name = payload.name
    payload.last_name = payload.last_name
    payload.email = EmailStr(payload.email.lower())

    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'status': 'success', 'message': 'Registration completed!'}


@router.post('/login')
def login(payload: schemas.UserLoginSchema, response: Response, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), ):
    user = db.query(models.User).filter(models.User.email ==
                                        EmailStr(payload.email.lower())).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Credentials')

    # if not user.verified:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')

    if not utilities.verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Credentials')

    access_token = Authorize.create_access_token(subject=str(
        user.id), fresh=True, expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(subject=str(
        user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    response.set_cookie('accessToken', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refreshToken', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('loggedIn', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return {'user': {'_id': user.id, 'name': user.name, 'email': user.email}, 'accessToken': access_token, 'refreshToken': refresh_token}


@router.get('/refresh')
def refresh_token(response: Response, request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized/Invalid token')

        user = db.query(models.User).filter(models.User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Invalid token or token expired')

        access_token = Authorize.create_access_token(subject=str(
            user.id), fresh=False, expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

        refresh_token = Authorize.create_refresh_token(subject=str(
            user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('refresh_token', refresh_token, REFRESH_TOKEN_EXPIRES_IN *
                        60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')

    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN *
                        60, ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return {'accessToken': access_token, 'refreshToken': refresh_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):

    Authorize.unset_jwt_cookies()

    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}
