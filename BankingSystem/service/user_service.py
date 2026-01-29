from sqlalchemy.orm import Session
from models.user import User
from models.account import Account
from security.security import get_password_hash, verify_password


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def delete_user(self, user_id: int):
        return self.db.delete(self.get_by_id(user_id))

    def create_user(self, data):
        user = User(
            name=data.name,
            surname=data.surname,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            role=data.role
        )
        self.db.add(user)
        self.db.flush()

        account = Account(user_id=user.id, _balance=0.0)
        self.db.add(account)

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
        return self.db.query(User).all()