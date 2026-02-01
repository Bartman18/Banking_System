from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, DeclarativeBase

from models.enums import TransactionType
from db.base import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)

    account = relationship("Account", backref="transactions")
    def __repr__(self):
        return f"Transaction(id={self.id}, type={self.transaction_type.name}, amount={self.amount})"

    def __str__(self):
        date_str = self.transaction_date.strftime("%Y-%m-%d %H:%M")
        return f"[{date_str}] {self.transaction_type.name}: {self.amount} PLN"
