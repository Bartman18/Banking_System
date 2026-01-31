from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship, DeclarativeBase
from db.base import Base

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    _balance = Column(Float, default=0)

    def __repr__(self):
        return f"Account(id={self.id}, user_id={self.user_id}, balance={self.balance})"

    def __str__(self):
        return f"Account nr {self.id} (Saldo: {self.balance:.2f} PLN)"

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance can't be negative")
        self._balance = value

