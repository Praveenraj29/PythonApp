from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud.crud_user import user as crud_user
from app.core.config import settings
from app.models import User
from app.schemas.user import UserCreate, UserCreateOpen
from app.tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def create_super_user(db: Session) -> User:
    email = settings.FIRST_SUPERUSER
    password = settings.FIRST_SUPERUSER_PASSWORD
    user_in = UserCreate(username=email, email=email, password=password, is_superuser=True, is_active=True)
    user = crud_user.create(db=db, obj_in=user_in)
    return user

def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateOpen(username=email, email=email, password=password)
    user = crud_user.create_user_open(db=db, obj_in=user_in)
    return user

def authentication_token_from_email(
    *, client: TestClient, email: str, password: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    user = crud_user.get_by_email(db=Session)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        crud_user.create_user_open(db, obj_in=user_in_create)
    return user_authentication_headers(client=client, email=email, password=password)