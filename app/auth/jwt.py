import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from typing import Union

from app.models.user_model import User
from app.schemas.user_schema import Token, UserSchema
from config import SECRET_KEY, ALGORITHM
from settings import pwd_context, redis_client, REFRESH_TOKEN_EXPIRE_DAYS


def verify_password(password, hashed_password) -> str:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=12)
    to_encode.update({"exp": expire, "type": "access"})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    token_id = uuid4()
    to_encode.update({"exp": expire,
                      "type": "refresh",
                      "token_id": str(token_id)
                      })
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def store_refresh_token(user_id: int, refresh_token: str, ttl: timedelta):
    # сохраниние токена в redis для дальнейшей его верификации
    key = f"refresh_token:{user_id}"
    redis_client.setex(key, ttl, refresh_token)


def verify_refresh_token(user_id: int, refresh_token):
    key = f"refresh_token:{user_id}"
    stored_token = redis_client.get(key)
    if stored_token is None or stored_token != refresh_token:
        return False
    return True


async def get_new_tokens(user: User, tokens: Union[Token, None] = None):
    '''
    создает одну функцию для получения обоих токенов

    '''
    user_data = UserSchema.from_orm(user)
    access_token = create_access_token({
        "sub": user_data.id})
    refresh_token = create_refresh_token({
        "sub": user_data.id})
    await store_refresh_token(user_data.id, refresh_token,
                              timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    return {
        "access": access_token,
        "refresh": refresh_token
    }
