import re
from typing import List, Dict
import io
import pypdf
from datetime import datetime

class PDFParser:
    @staticmethod
    def parse(file_content: bytes) -> List[Dict]:
        """
        Parses the Chase Bank Statement PDF.
        Extracts: Date, Description, Amount
        """
        reader = pypdf.PdfReader(io.BytesIO(file_content))
        transactions = []

        # Regex for line item: "MM/DD/YYYY  Description  $1,234.56"
        # The screenshot shows: 01/03/2025  Amazon Purchase  $45.67
        # Note: Description might contain spaces. Amount is at the end.

        # Pattern: Date (MM/DD/YYYY) + Space + Description + Space + Amount ($xx.xx)
        # Note: In PDF text extraction, columns might just be separated by spaces.
        # Let's try a robust regex.

        pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+\$([\d,]+\.\d{2})")

        for page in reader.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                match = pattern.search(line)
                if match:
                    date_str, description, amount_str = match.groups()

                    try:
                        date_obj = datetime.strptime(date_str, "%m/%d/%Y").date()
                        amount = float(amount_str.replace(',', ''))

                        transactions.append({
                            "date": date_obj,
                            "description": description.strip(),
                            "amount": amount,
                            "source": "pdf_statement",
                            # These fields need manual input later
                            "category": "Uncategorized",
                            "spender": "Shared", # Default
                            "payer": "", # To be filled from global context
                            "owed_amount": 0.0,
                            "comment": ""
                        })
                    except ValueError:
                        continue # Skip malformed lines

        return transactions
