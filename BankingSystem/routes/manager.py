from fastapi import Depends, APIRouter, HTTPException

from schemas.transaction import TransactionOut
from security.exception import UserAlreadyExists, InvalidAmount, UserNotFound, AccountNotFound
from service.user_service import UserService
from service.account_service import AccountService
from db.database_dependencies import get_db
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from security.deps import require_manager
from typing import List

router = APIRouter(prefix="/manager", tags=["Manager"], dependencies=[Depends(require_manager)])


@router.delete("/delete/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        UserService(db).delete_user(customer_id)
        return {"message": "User deleted"}
    except UserNotFound:
        raise HTTPException(404, "User not found")


@router.post('/create/user/')
def add_client(data: UserCreate, db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        user = service.create_user(data)

        return UserResponse(
            id=user.id,

            email=user.email,
            role=user.role,
            full_name=user.full_name()
        )
    except UserAlreadyExists:
        raise HTTPException(400, detail="User already exists")
    except Exception as e:
        raise HTTPException(500)


@router.get('/all_transactions_list/', response_model=List[TransactionOut])
def all_transaction(db: Session = Depends(get_db)):
    try:
        service = AccountService(db)
        transactions = service.all_transactions()

        transactions_out = [
            TransactionOut(
                id=t.id,
                # account_id=t.account_id,
                amount=t.amount,
                transaction_type=t.transaction_type,
                transaction_date=t.transaction_date,
                user_name=t.account.user.full_name()
            )
            for t in transactions
        ]
        return transactions_out
    except AccountNotFound:
        raise HTTPException(404, "Account not found")




@router.get("/{customer_id}/")
def get_user(customer_id: int, db: Session = Depends(get_db)):
    try:

        user = UserService(db).get_by_id(customer_id)
        return UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            full_name=user.full_name()

        )
    except UserNotFound:
        raise HTTPException(404, "User not found")


@router.post("/all_customers/")
def get_all_client(db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.get_all_users()

    result = []
    for u in users:
        account = service.get_user_account(u.id)
        result.append({
            "id": u.id,
            "name": u.name,
            "surname": u.surname,
            "email": u.email,
            "role": u.role.value,
            "full_name": u.full_name(),
            "account_id": account.id if account else None,
            "balance": account.balance if account else None
        })

    return result
