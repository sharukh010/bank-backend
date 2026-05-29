import database


def create_account(name: str):
    account = {
        "id": database.account_id_seq,
        "name": name,
        "balance": 0.0
    }
    database.accounts.append(account)
    database.account_id_seq += 1
    return account


def deposit(account_id: int, amount: float):
    acc = next((a for a in database.accounts if a["id"] == account_id), None)
    if not acc:
        return None
    acc["balance"] += amount
    return acc


def withdraw(account_id: int, amount: float):
    acc = next((a for a in database.accounts if a["id"] == account_id), None)
    if not acc or acc["balance"] < amount:
        return None
    acc["balance"] -= amount
    return acc


def transfer(from_account: int, to_account: int, amount: float):
    sender = next((a for a in database.accounts if a["id"] == from_account), None)
    receiver = next((a for a in database.accounts if a["id"] == to_account), None)
    if not sender or not receiver or sender["balance"] < amount:
        return None
    sender["balance"] -= amount
    receiver["balance"] += amount
    return {"from": sender, "to": receiver}


def apply_loan(account_id: int, amount: float):
    loan = {
        "id": database.loan_id_seq,
        "account_id": account_id,
        "amount": amount,
        "status": "Pending"
    }
    database.loans.append(loan)
    database.loan_id_seq += 1
    return loan


def approve_loan(loan_id: int):
    loan = next((l for l in database.loans if l["id"] == loan_id), None)
    if not loan:
        return None
    if loan["status"] == "Approved":
        return {"error": "Loan already approved"}
    loan["status"] = "Approved"
    acc = next((a for a in database.accounts if a["id"] == loan["account_id"]), None)
    acc["balance"] += loan["amount"]
    return {"loan": loan, "account": acc}


def get_balance(account_id: int):
    acc = next((a for a in database.accounts if a["id"] == account_id), None)
    if not acc:
        return None
    return acc["balance"]
