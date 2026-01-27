from pydantic import BaseModel, ConfigDict
from datetime import datetime
from BankingSystem.models.enums import TransactionType


class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType


class TransactionOut(TransactionCreate):
    id: int
    account_id: int
    timestamp: datetime



