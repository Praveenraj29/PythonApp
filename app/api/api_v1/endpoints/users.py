from typing import Any

from fastapi import APIRouter, Depends, HTTPException


from app.crud.crud_user import user as crud
from app.api.deps import (
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.schemas.user import UserCreate, UserCreateOpen, UserOut


router = APIRouter()



@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserOut
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = crud.get_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = crud.create(db=session, obj_in=user_in)
    return user



@router.post("/open", response_model=UserOut)
def create_user_open(session: SessionDep, user_in: UserCreateOpen) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.get_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.create_user_open(db=session, obj_in=user_in)
    return user