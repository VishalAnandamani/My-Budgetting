import pandas as pd
from typing import List, Dict
import io
from datetime import datetime

class CSVParser:
    REQUIRED_COLUMNS = [
        "Date", "Expense", "Spender", "Category",
        "Paid By", "Amount", "Amount Owed", "Comment"
    ]

    @staticmethod
    def parse(file_content: bytes) -> List[Dict]:
        """
        Parses the historical CSV data.
        """
        try:
            df = pd.read_csv(io.BytesIO(file_content))

            # Normalize column names: strip whitespace
            df.columns = [c.strip() for c in df.columns]

            # Basic validation
            missing_cols = [col for col in CSVParser.REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing columns: {missing_cols}")

            transactions = []

            # Clean string columns
            string_cols = ["Expense", "Spender", "Category", "Paid By", "Comment"]
            for col in string_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()

            for _, row in df.iterrows():
                # Handle date parsing - assuming standard formats, but user said "Use mock we will see later"
                # I'll try to handle basic formats
                date_str = str(row["Date"])
                try:
                    # Try ISO first, then US format
                    parsed_date = pd.to_datetime(date_str).date()
                except:
                    # Fallback or keep as is? Better to fail fast or set None.
                    # For MVP, let's assume it works or fail.
                    parsed_date = None

                amount = float(str(row["Amount"]).replace('$', '').replace(',', ''))
                owed = float(str(row["Amount Owed"]).replace('$', '').replace(',', '')) if pd.notna(row["Amount Owed"]) else 0.0

                transactions.append({
                    "date": parsed_date,
                    "description": row["Expense"],
                    "category": row["Category"],
                    "spender": row["Spender"],
                    "payer": row["Paid By"],
                    "amount": amount,
                    "owed_amount": owed,
                    "comment": row["Comment"] if pd.notna(row["Comment"]) else "",
                    "source": "csv_import"
                })

            return transactions

        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")
