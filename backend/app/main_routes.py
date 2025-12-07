from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas
from app.services.parser_csv import CSVParser
from app.services.parser_pdf import PDFParser
from app.services.finance import calculate_owed

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/history")
async def upload_history(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        transactions_data = CSVParser.parse(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    saved_count = 0
    for data in transactions_data:
        # Create DB object
        # Note: CSV parser returns dict with snake_case keys matching model attributes
        # We need to ensure date is valid.
        if not data.get("date"):
            continue # Skip invalid dates for now

        db_txn = models.Transaction(**data)
        db.add(db_txn)
        saved_count += 1

    db.commit()
    return {"message": f"Successfully imported {saved_count} transactions"}

@router.post("/upload/statement", response_model=List[schemas.TransactionCreate])
async def upload_statement(file: UploadFile = File(...)):
    content = await file.read()
    try:
        # Returns list of dicts.
        # Note: PDF parser returns partial data. Frontend needs to fill the rest.
        # We return them as is, frontend will send them back to /transactions/bulk
        transactions_data = PDFParser.parse(content)
        return transactions_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transactions/bulk")
async def create_transactions_bulk(transactions: List[schemas.TransactionCreate], db: Session = Depends(get_db)):
    for txn_data in transactions:
        # Recalculate owed amount on server side to be safe, or trust frontend?
        # Let's trust frontend for MVP but verify logic.
        # Actually, let's enforce server logic for consistency.

        # We'll take the provided payer/spender/amount and re-calc owed.
        # This ensures the business logic is the source of truth.
        txn_dict = txn_data.dict()
        txn_dict["owed_amount"] = calculate_owed(
            txn_dict["amount"],
            txn_dict["payer"],
            txn_dict["spender"]
        )

        db_txn = models.Transaction(**txn_dict)
        db.add(db_txn)

    db.commit()
    return {"message": "Transactions saved successfully"}

@router.get("/transactions", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    # 1. Spending by Category
    # 2. Debt Summary

    # We can do this with SQL aggregation or python for simplicity in MVP
    transactions = db.query(models.Transaction).all()

    category_totals = {}
    debts = {"Vishal": 0.0, "Gouthami": 0.0} # Positive means they are OWED money. Negative means they OWE.

    for t in transactions:
        # Category stats
        cat = t.category or "Uncategorized"
        category_totals[cat] = category_totals.get(cat, 0.0) + t.amount

        # Debt stats
        # If t.owed_amount > 0:
        #   It means 'spender' owes 'payer'.
        #   Payer gets +owed_amount
        #   Spender gets -owed_amount

        # Handle "Shared" logic mapping to actual people
        # Logic is: calculate_owed returns how much is owed TO the payer.
        # Who owes it?
        # If spender is "Shared" -> The OTHER person owes.
        # If spender is Person B -> Person B owes.

        owed = t.owed_amount
        payer = t.payer
        spender = t.spender

        if owed > 0:
            # Credit the payer
            if payer in debts:
                debts[payer] += owed

            # Debit the debtor
            debtor = None
            if spender == "Shared":
                # If Vishal paid for Shared, Gouthami owes.
                debtor = "Gouthami" if payer == "Vishal" else "Vishal"
            else:
                debtor = spender

            if debtor and debtor in debts:
                debts[debtor] -= owed

    # Simplify debt to "Who owes whom?"
    # If Vishal = +100 (Owed 100), Gouthami = -100 (Owes 100) -> Gouthami owes Vishal 100.

    net_vishal = debts["Vishal"]
    debt_summary = []

    if net_vishal > 0:
        debt_summary.append({
            "debtor": "Gouthami",
            "creditor": "Vishal",
            "amount": round(net_vishal, 2)
        })
    elif net_vishal < 0:
        debt_summary.append({
            "debtor": "Vishal",
            "creditor": "Gouthami",
            "amount": round(abs(net_vishal), 2)
        })

    return {
        "spending_by_category": [{"category": k, "total": round(v, 2)} for k, v in category_totals.items()],
        "debt_summary": debt_summary
    }
