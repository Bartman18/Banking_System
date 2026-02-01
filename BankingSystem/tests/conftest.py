import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from schemas.user import UserCreate
from models.enums import UserRole
from models.user import User
from models.account import Account

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
        role=UserRole.CUSTOMER,
        initial_balance=0,
    )


@pytest.fixture
def test_user(db_session):
    user = User(
        name="Test",
        surname="User",
        email="test@example.com",
        hashed_password="hashed_password",
        role=UserRole.CUSTOMER,
        initial_balance=0.0
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_account(db_session, test_user):
    account = Account(user_id=test_user.id, _balance=100.0)
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)
    return account