from sqlalchemy.orm import Session
import models


def create_account(db: Session, name: str):
    account = models.Account(name=name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def deposit(db: Session, account_id: int, amount: float):
    acc = db.query(models.Account).filter(models.Account.id == account_id).first()
    acc.balance += amount
    db.commit()
    db.refresh(acc)
    return acc


def withdraw(db: Session, account_id: int, amount: float):
    acc = db.query(models.Account).filter(models.Account.id == account_id).first()
    if acc.balance < amount:
        return None
    acc.balance -= amount
    db.commit()
    db.refresh(acc)
    return acc


def transfer(db: Session, from_acc: int, to_acc: int, amount: float):
    sender = db.query(models.Account).filter(models.Account.id == from_acc).first()
    receiver = db.query(models.Account).filter(models.Account.id == to_acc).first()

    if sender.balance < amount:
        return None

    sender.balance -= amount
    receiver.balance += amount
    db.commit()
    db.refresh(sender)
    db.refresh(receiver)
    return {"from": sender, "to": receiver}


def apply_loan(db: Session, account_id: int, amount: float):
    loan = models.Loan(account_id=account_id, amount=amount)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def approve_loan(db: Session, loan_id: int):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        return None
    if loan.status == "Approved":
        return {"error": "Loan already approved"}
    loan.status = "Approved"
    acc = db.query(models.Account).filter(models.Account.id == loan.account_id).first()
    acc.balance += loan.amount
    db.commit()
    db.refresh(loan)
    db.refresh(acc)
    return {"loan": loan, "account": acc}


def get_balance(db: Session, account_id: int):
    acc = db.query(models.Account).filter(models.Account.id == account_id).first()
    return acc.balance