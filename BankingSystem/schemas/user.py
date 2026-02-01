from pydantic import BaseModel, EmailStr, ConfigDict
from models.enums import UserRole


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER
    initial_balance: float




class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    full_name: str
