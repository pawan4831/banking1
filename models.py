from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), unique=True, index=True)
    balance = Column(Float, default=0.0)
    def __repr__(self):
        return f"<Account(account_number={self.account_number}, balance={self.balance})>"

