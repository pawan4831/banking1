from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, init_db
from models import Account
app = FastAPI()
init_db()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    #pydantic schema
class AccountCreate(BaseModel):
    account_number: str
    total_balance: float
class AccountResponse(BaseModel):
    account_number: str
    balance: float
class WithdrawRequest(BaseModel):
    amount: float
    #fastAPI's
@app.post("/accounts/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = Account(account_number=account.account_number, balance=account.total_balance)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return AccountResponse(account_number=db_account.account_number, balance=db_account.balance)
@app.get("/accounts/{account_number}", response_model=AccountResponse)
def get_account(account_number: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse(account_number=account.account_number, balance=account.balance)
@app.post("/accounts/{account_number}/withdraw/", response_model=AccountResponse)
def withdraw(account_number: str, withdraw_request: WithdrawRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if withdraw_request.amount > account.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    account.balance -= withdraw_request.amount
    db.commit()
    return AccountResponse(account_number=account.account_number, balance=account.balance)
