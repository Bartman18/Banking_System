from sqlalchemy.orm import Session
from models.user import User
from models.account import Account
from security.security import get_password_hash, verify_password
from schemas.user import UserResponse
from security.exception import UserAlreadyExists, InvalidAmount, UserNotFound
from service.account_service import AccountService


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise UserNotFound()

        self.db.delete(user)
        self.db.commit()

    def create_user(self, data):
        existing_user = self.get_by_email(data.email)
        if existing_user:
            raise UserAlreadyExists()

        initial_balance = data.initial_balance
        if initial_balance < 0:
            raise InvalidAmount(initial_balance, "Initial balance cannot be negative")

        user = User(
            name=data.name,
            surname=data.surname,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            role=data.role,
            initial_balance=data.initial_balance
        )

        self.db.add(user)
        self.db.flush()

        account_service = AccountService(self.db)
        account = account_service.create_account(user.id, data.initial_balance)


        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str):
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_all_users(self):
        user = self.db.query(User).all()
        return user

    def get_user_account(self, user_id: int) -> Account | None:
        return self.db.query(Account).filter(Account.user_id == user_id).first()
