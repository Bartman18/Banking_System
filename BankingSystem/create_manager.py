from BankingSystem.db.session import SessionLocal
from BankingSystem.models.user import User
from BankingSystem.models.enums import UserRole
from BankingSystem.security.security import get_password_hash

def run():
    db = SessionLocal()

    user = User(
        name="Jan",
        surname="Kowalski",
        email="manager@example.com",
        hashed_password=get_password_hash("haslo123"),
        role=UserRole.MANAGER
    )

    db.add(user)
    db.commit()
    db.refresh(user)



if __name__ == "__main__":
    run()
