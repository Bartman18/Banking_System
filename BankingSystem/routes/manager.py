from fastapi import Depends, APIRouter, HTTPException
from service.user_service import UserService
from service.account_service import AccountService
from db.database_dependencies import get_db
from sqlalchemy.orm import Session
from schemas.user import UserCreate,UserResponse
from security.deps import require_manager
router = APIRouter(prefix="/manager", tags=["Manager"]), dependencies=[Depends(require_manager)]


@router.delete("/delete/{customer_id}")
def delete_customer(user_id:int, db:Session = Depends(get_db)):
    
    UserService(db).delete_user(user_id)
    


@router.post('create/user/')
def add_client(data:UserCreate, db:Session = Depends(get_db)):
    service = UserService(db)

    if service.get_by_email(data.email):
        raise HTTPException(400, "Email is already registered")

    user = service.create_user(data)

    return UserResponse(
        id=user.id,
        
        email=user.email,
        role=user.role,
        full_name = user.full_name()

    )

@router.get("/{customer_id}")
def get_user(user_id:int ,db:Session = Depends(get_db)):
    user = UserService(db).get_by_id(user_id)
    if not user:
        raise HTTPException(400, "User not exist")
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        full_name = user.full_name()

    )


@router.get('/all_transaction/')
def all_transaction(db:Session = Depends(get_db)):
    service = AccountService(db)
    transaction = service.all_transaction()
    return [
        {
            "id":t.id,
            "account_id":t.account_id,
            "amount":t.amount,
            "type":t.transaction_type.value,
            "date":t.transaction_date
        }
        for t in transaction
    ]
    
@router.post("/all_customers/")
def get_all_client(db:Session = Depends(get_db)):
    user = UserService(db).get_all_users()
    return [
        UserResponse(
            id=x.id,
            email=x.email,
            role=x.role,
            full_name = x.full_name()

        ) for x in user
    ]
@router.post("/")
def balanace():
    pass


