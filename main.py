from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import schemas, services

app = FastAPI(title="Bank Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 1. Account Creation
@app.post("/create-account")
def create_account(data: schemas.AccountCreate):
    return services.create_account(data.name)


# 2. Deposit
@app.post("/deposit")
def deposit(data: schemas.Transaction):
    result = services.deposit(data.account_id, data.amount)
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result


# 3. Withdraw
@app.post("/withdraw")
def withdraw(data: schemas.Transaction):
    result = services.withdraw(data.account_id, data.amount)
    if not result:
        raise HTTPException(status_code=400, detail="Insufficient balance or account not found")
    return result


# 4. Transfer Money
@app.post("/transfer")
def transfer(data: schemas.Transfer):
    result = services.transfer(data.from_account, data.to_account, data.amount)
    if not result:
        raise HTTPException(status_code=400, detail="Transfer failed")
    return result


# 5. Apply Loan
@app.post("/loan")
def apply_loan(data: schemas.LoanApply):
    return services.apply_loan(data.account_id, data.amount)


# 6. Approve Loan
@app.post("/loan/{loan_id}/approve")
def approve_loan(loan_id: int):
    result = services.approve_loan(loan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Loan not found")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# 7. Check Balance
@app.get("/balance/{account_id}")
def get_balance(account_id: int):
    balance = services.get_balance(account_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": balance}
