from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from models.account import Account
from models.transaction import Transaction
from models.enums import TransactionType


class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def get_account(self, account_id: int) -> Account:
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(404, "Account not found")
        return account

    def get_account_by_user_id(self, user_id: int) -> Account:
        account = self.db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(404, "Account not found for this user")
        return account

    def deposit(self, account_id: int, amount: float):
        if amount <= 0:
            raise HTTPException(400, "Amount must be positive")

        account = self.get_account(account_id)
        account.balance += amount

        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            transaction_date=datetime.utcnow()
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(account)

        return account

    def withdraw(self, account_id: int, amount: float):
        if amount <= 0:
            raise HTTPException(400, "Amount must be positive")

        account = self.get_account(account_id)

        if account.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        account.balance -= amount

        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.WITHDRAWAL,
            transaction_date=datetime.utcnow()
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(account)

        return account

    def get_transactions(self, account_id: int):
        account = self.get_account(account_id)
        return self.db.query(Transaction).filter(Transaction.account_id == account_id).order_by(
            Transaction.transaction_date).all()

    def create_account(self, user_id: int) -> Account:
        account = Account(user_id=user_id, _balance=0.0)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
