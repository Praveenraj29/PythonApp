from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import StaticPool, create_engine
from app.core.config import settings
from app.main import app as fastapi_app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, password="Testing@123", db=db
    )