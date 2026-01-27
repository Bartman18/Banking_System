from pydantic import BaseModel, EmailStr, ConfigDict
from BankingSystem.models.enums import UserRole





class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    role: UserRole
    full_name: str


