
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from schemas.user import UserCreate
from service.user_service import UserService
from models.enums import UserRole

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_data():
    return UserCreate(
        name="Test",
        surname="Nazwisko",
        email="test@example.com",
        password="test123",
        role = UserRole.CUSTOMER,
        initial_balance = 0,
    )


class TestUserService:

    def test_create_user(self, db_session, user_data):
        service = UserService(db_session)
        user= service.create_user(user_data)

        assert user.id is not None
        assert user.email == "test@example.com"
