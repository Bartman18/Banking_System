import enum


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    MANAGER = "manager"


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

