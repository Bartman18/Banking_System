from sqlalchemy.orm import Session

from models.enums import TransactionType
from schemas.transaction import TransactionCreate
from datetime import datetime
from models.transaction import Transaction

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def save_transaction(self, account_id, amount, transaction_type: TransactionType ):
        if not account_id or not amount:
            raise Exception("Account and amount cannot be null")

        transaction = Transaction(
            account_id=account_id,
            amount=amount,
            transaction_type=transaction_type,
            transaction_date=datetime.utcnow()
        )

        self.db.add(transaction)

        return transaction
