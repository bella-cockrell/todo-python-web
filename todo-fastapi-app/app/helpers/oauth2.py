from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

# import gateways
from app.gateways.users_gateway import get_user
# import models
from app.models.user_models import UserInDBModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# randomly generated key
SECRET_KEY = "402af2408c510819c72aef58836c6a7e12e9af0c1a21bfa45c14dd20ef869563"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(fake_db, username: str, password: str) -> UserInDBModel | bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
