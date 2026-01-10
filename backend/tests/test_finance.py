import unittest
from app.services.finance import calculate_owed

class TestFinanceLogic(unittest.TestCase):

    def test_shared_expense(self):
        # Vishal pays 100 for Shared -> Gouthami owes 50
        self.assertEqual(calculate_owed(100.0, "Vishal", "Shared"), 50.0)
        # Gouthami pays 50 for Shared -> Vishal owes 25
        self.assertEqual(calculate_owed(50.0, "Gouthami", "Shared"), 25.0)

    def test_personal_expense_paid_by_self(self):
        # Vishal pays 100 for Vishal -> 0 owed
        self.assertEqual(calculate_owed(100.0, "Vishal", "Vishal"), 0.0)
        # Gouthami pays 50 for Gouthami -> 0 owed
        self.assertEqual(calculate_owed(50.0, "Gouthami", "Gouthami"), 0.0)

    def test_personal_expense_paid_by_other(self):
        # Vishal pays 100 for Gouthami -> Gouthami owes 100
        self.assertEqual(calculate_owed(100.0, "Vishal", "Gouthami"), 100.0)
        # Gouthami pays 50 for Vishal -> Vishal owes 50
        self.assertEqual(calculate_owed(50.0, "Gouthami", "Vishal"), 50.0)

if __name__ == '__main__':
    unittest.main()
