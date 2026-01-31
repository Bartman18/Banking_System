from fastapi import Depends, APIRouter
from service.user_service import UserService
from security.deps import require_client, get_current_user
from db.database_dependencies import get_db
from sqlalchemy.orm import Session
from schemas.transaction import TransactionType
from schemas.user import UserResponse
from service.account_service import AccountService
from models.user import User


router = APIRouter(prefix="/customer", tags=["Customer"])






@router.post('/transaction/')
def transaction(data:TransactionType ,amount:float, db:Session = Depends(get_db), user: User = Depends(require_client)):
    
    service = AccountService(db)
    account = service.get_account_by_user_id(user.id)

    if data == TransactionType.WITHDRAWAL:
        return service.withdraw(account.id, amount)
    elif data == TransactionType.DEPOSIT:
        return service.deposit(account.id, amount)

    else:
        raise HTTP_401_UNAUTHORIZED


@router.get('/transaction_history/')
def transaction_history(db:Session = Depends(get_db),user: User = Depends(require_client)):
    service = AccountService(db)
    account = service.get_account(user.id)
    transaction = service.get_transactions(account.id)
    return [
        {
            "id":t.id,
            "amount":t.amount,
            "type":t.transaction_type.value,
            "date":t.transaction_date
        }
        for t in transaction
    ]


@router.get('/current_balance/')
def get_balance(db:Session = Depends(get_db), user:User = Depends(require_client)):
    account = AccountService(db).get_account_by_user_id(user.id)
    return {"balance":account.balance}
    
    


@router.get('/statment/')
def statment():
    pass
