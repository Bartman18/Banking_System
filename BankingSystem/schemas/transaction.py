from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models.enums import TransactionType


class TransactionCreate(BaseModel):
    amount: float
    account_id: int
    type: TransactionType
    transaction_date: datetime


class TransactionOut(BaseModel):
    id: int
    amount: float
    account_id:int
    # user_name: str
    transaction_type: TransactionType
    transaction_date: datetime
