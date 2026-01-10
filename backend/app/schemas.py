from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class TransactionBase(BaseModel):
    date: Optional[date]
    description: str
    category: str
    spender: str
    payer: str
    amount: float
    owed_amount: float
    comment: Optional[str] = None
    source: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True

class StatsCategory(BaseModel):
    category: str
    total: float

class StatsDebt(BaseModel):
    debtor: str
    creditor: str
    amount: float
