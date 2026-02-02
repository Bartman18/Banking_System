from fastapi import Depends, APIRouter, HTTPException
from security.exception import AccountNotFound, InvalidAmount, InsufficientFunds
from service.user_service import UserService
from security.deps import require_client, get_current_user
from db.database_dependencies import get_db
from sqlalchemy.orm import Session
from schemas.transaction import TransactionType, TransactionOut
from schemas.user import UserResponse
from service.account_service import AccountService
from models.user import User
from typing import List

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.post('/transaction/')
def transaction(data: TransactionType, amount: float, db: Session = Depends(get_db),
                user: User = Depends(require_client)):
    service = AccountService(db)
    account = service.get_account_by_user_id(user.id)
    try:
        if data == TransactionType.WITHDRAWAL:
            return service.withdraw(account.id, amount)
        elif data == TransactionType.DEPOSIT:
            return service.deposit(account.id, amount)
        else:
            raise HTTPException(400, "Invalid transaction type")
    except AccountNotFound:
        raise HTTPException(400, "Account not found")
    except InvalidAmount:
        raise HTTPException(400, "Invalid amount")
    except InsufficientFunds:
        raise HTTPException(400, "Insufficient funds")


@router.get('/transaction_history/', response_model=List[TransactionOut])
def transaction_history(db: Session = Depends(get_db), user: User = Depends(require_client)):
    try:
        service = AccountService(db)
        account = service.get_account_by_user_id(user.id)
        transactions = service.get_transactions(account.id)

        transactions_out = [
            TransactionOut(
                id=t.id,
                account_id=t.account_id,
                amount=t.amount,
                transaction_type=t.transaction_type,
                transaction_date=t.transaction_date,
                # user_name=t.account.user.full_name()
            )
            for t in transactions
        ]
        return transactions_out
    except AccountNotFound:
        raise HTTPException(404, "Account not found")


@router.get('/current_balance/')
def get_balance(db: Session = Depends(get_db), user: User = Depends(require_client)):
    try:
        account = AccountService(db).get_account_by_user_id(user.id)
        return {"balance": account.balance}
    except AccountNotFound:
        raise HTTPException(404, "Account not found")
