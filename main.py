from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, services
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Backend API")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Account Creation
@app.post("/create-account")
def create_account(data: schemas.AccountCreate, db: Session = Depends(get_db)):
    return services.create_account(db, data.name)


# 2. Deposit
@app.post("/deposit")
def deposit(data: schemas.Transaction, db: Session = Depends(get_db)):
    return services.deposit(db, data.account_id, data.amount)


# 3. Withdraw
@app.post("/withdraw")
def withdraw(data: schemas.Transaction, db: Session = Depends(get_db)):
    result = services.withdraw(db, data.account_id, data.amount)
    if not result:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    return result


# 4. Transfer Money
@app.post("/transfer")
def transfer(data: schemas.Transfer, db: Session = Depends(get_db)):
    result = services.transfer(db, data.from_account, data.to_account, data.amount)
    if not result:
        raise HTTPException(status_code=400, detail="Transfer failed")
    return result


# 5. Apply Loan
@app.post("/loan")
def apply_loan(data: schemas.LoanApply, db: Session = Depends(get_db)):
    return services.apply_loan(db, data.account_id, data.amount)


# 6. Check Balance
@app.get("/balance/{account_id}")
def get_balance(account_id: int, db: Session = Depends(get_db)):
    return {"balance": services.get_balance(db, account_id)}