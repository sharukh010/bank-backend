from pydantic import BaseModel

class AccountCreate(BaseModel):
    name: str


class Transaction(BaseModel):
    account_id: int
    amount: float


class Transfer(BaseModel):
    from_account: int
    to_account: int
    amount: float


class LoanApply(BaseModel):
    account_id: int
    amount: float