from sqlalchemy.orm import Session

from app.crud.crud_user import user as crud
from app.core.config import settings
from app.schemas.user import UserCreate  # noqa: F401


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.get_by_email(db=session, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.create(db=session, obj_in=user_in)