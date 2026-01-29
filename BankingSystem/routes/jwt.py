from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from db.database_dependencies import get_db
from security.security import create_access_token
from service.user_service import UserService
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    service = UserService(db)
    user = service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(user.id, user.role.value)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)

    if service.get_by_email(user.email):
        raise HTTPException(400, "Email already registered")

    created_user = service.create_user(user)

    return UserResponse(
        id=created_user.id,
        name=created_user.name,
        surname=created_user.surname,
        email=created_user.email,
        role=created_user.role,
        full_name=created_user.full_name()
    )