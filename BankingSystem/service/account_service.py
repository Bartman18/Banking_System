from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from models.account import Account
from models.transaction import Transaction
from models.enums import TransactionType
from security.exception import AccountNotFound, InsufficientFunds, InvalidAmount
from service.transaction_service import TransactionService


class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def get_account(self, account_id: int) -> Account:
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise AccountNotFound()
        return account

    def get_account_by_user_id(self, user_id: int) -> Account:
        account = self.db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise AccountNotFound()
        return account

    def deposit(self, account_id: int, amount: float):
        if amount <= 0:
            raise InvalidAmount()

        account = self.get_account(account_id)
        account.balance += amount

        transaction_service = TransactionService(self.db)
        transaction = transaction_service.save_transaction(account_id, amount, TransactionType.DEPOSIT)

        self.db.commit()
        self.db.refresh(account)

        return account

    def withdraw(self, account_id: int, amount: float):
        if amount <= 0:
            raise InvalidAmount

        account = self.get_account(account_id)
        transaction_service = TransactionService(self.db)

        if account.balance < amount:
            raise InsufficientFunds()

        account.balance -= amount

        transaction = transaction_service.save_transaction(account_id, amount, TransactionType.WITHDRAWAL)

        self.db.commit()
        self.db.refresh(account)

        return account

    def get_transactions(self, account_id: int):
        # account = self.get_account(account_id)
        return self.db.query(Transaction).filter(Transaction.account_id == account_id).order_by(
            Transaction.transaction_date).all()

    def all_transactions(self):
        return self.db.query(Transaction).order_by(
            Transaction.transaction_date).all()

    def create_account(self, user_id: int, initial_balance: float = 0.0) -> Account:

        if initial_balance < 0:
            raise InvalidAmount(initial_balance, "Initial balance cannot be negative")

        account = Account(user_id=user_id, _balance=initial_balance)
        self.db.add(account)
        self.db.flush()

        if initial_balance > 0:
            transaction_service = TransactionService(self.db)
            transaction_service.save_transaction(account.id, initial_balance, TransactionType.DEPOSIT)

        return account
