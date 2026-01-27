from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from BankingSystem.models.enums import UserRole
from BankingSystem.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))

    def full_name(self):
        return self.name + ' ' + self.surname

    def __repr__(self):
        return f"User(id={self.id}, name={self.full_name()}, role={self.role})"

    def __str__(self):
        return f"User: {self.email} [{self.role}]"
