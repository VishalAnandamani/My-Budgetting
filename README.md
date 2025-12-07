# My-Budgeting

A personal finance application to track expenses, categorize spending, and calculate shared debts between family members.

## Features

-   **Data Import**:
    -   Historical data via CSV upload.
    -   Bank statements via PDF upload (currently supports Chase format).
-   **Debt Calculation**:
    -   Automatically calculates "Who owes Whom" based on Payer vs. Spender.
    -   Handles "Shared" expenses (50/50 split).
-   **Dashboard**:
    -   Spending by Category visualization.
    -   Net Debt Summary (Settlement).
-   **Tech Stack**:
    -   **Backend**: Python FastAPI, SQLAlchemy (SQLite).
    -   **Frontend**: React, TypeScript, TailwindCSS, Recharts.

## Project Structure

```
├── backend/            # FastAPI application
│   ├── app/
│   │   ├── services/   # Business logic & parsers
│   │   ├── models.py   # Database schema
│   │   └── ...
│   └── finance.db      # SQLite database (auto-created)
├── frontend/           # React application
│   ├── src/
│   └── ...
└── ...
```

## Getting Started

### Prerequisites

-   Python 3.10+
-   Node.js 18+

### 1. Backend Setup

Open a terminal and navigate to the `backend` directory:

```bash
cd backend
```

Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
# Or manually:
pip install fastapi uvicorn sqlalchemy pydantic pandas pypdf python-multipart
```

Run the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

### 3. Running the Application

1.  Open `http://localhost:5173` in your browser.
2.  Click **+ Upload Data**.
3.  Choose **Historical Data (CSV)** for spreadsheet imports or **New Statement (PDF)** for bank PDFs.
4.  Review the transactions and click **Save All**.
5.  View your spending insights on the Dashboard.

## Data Formats

**CSV Import (Historical)**
Expected columns: `Date`, `Expense`, `Spender`, `Category`, `Paid By`, `Amount`, `Amount Owed`, `Comment`.

**PDF Import**
Currently optimized for Chase Credit Card statements (Format: `MM/DD/YYYY Description $Amount`).
