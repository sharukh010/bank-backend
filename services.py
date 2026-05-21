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
    return acc


def withdraw(db: Session, account_id: int, amount: float):
    acc = db.query(models.Account).filter(models.Account.id == account_id).first()
    if acc.balance < amount:
        return None
    acc.balance -= amount
    db.commit()
    return acc


def transfer(db: Session, from_acc: int, to_acc: int, amount: float):
    sender = db.query(models.Account).filter(models.Account.id == from_acc).first()
    receiver = db.query(models.Account).filter(models.Account.id == to_acc).first()

    if sender.balance < amount:
        return None

    sender.balance -= amount
    receiver.balance += amount
    db.commit()
    return {"from": sender, "to": receiver}


def apply_loan(db: Session, account_id: int, amount: float):
    loan = models.Loan(account_id=account_id, amount=amount)
    db.add(loan)
    db.commit()
    return loan


def get_balance(db: Session, account_id: int):
    acc = db.query(models.Account).filter(models.Account.id == account_id).first()
    return acc.balance