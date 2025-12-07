from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    description = Column(String)  # Expense description
    category = Column(String, index=True)
    spender = Column(String, index=True)  # Who Spent: "Vishal", "Gouthami", "Shared"
    payer = Column(String, index=True)    # Who Paid: "Vishal", "Gouthami"
    amount = Column(Float)
    owed_amount = Column(Float) # How much the non-payer owes the payer (or split logic)
    comment = Column(String, nullable=True)

    # Metadata to track origin
    source = Column(String) # "csv_import" or "pdf_statement"
