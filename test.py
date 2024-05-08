import os
import unittest

from main import AccountManager, Transaction


class TestAccountManager(unittest.TestCase):
    def setUp(self):
        self.filename = "test_transactions.csv"
        self.account_manager = AccountManager(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_add_transaction(self):
        test_transaction = Transaction(
            "2024-05-01", "Доход", 1000, "Тестовое описание"
        )

        self.account_manager.add_transaction(test_transaction)

        transactions = self.account_manager.load_transactions()

        self.assertEqual(len(transactions), 1)

        added_transaction = transactions[0]
        self.assertEqual(added_transaction[0], "2024-05-01")
        self.assertEqual(added_transaction[1], "Доход")
        self.assertEqual(int(added_transaction[2]), 1000)
        self.assertEqual(added_transaction[3], "Тестовое описание")

    def test_edit_transaction(self):
        test_transaction1 = Transaction(
            "2024-05-01", "Доход", 1000, "Тестовое описание 1"
        )
        test_transaction2 = Transaction(
            "2024-05-02", "Расход", 500, "Тестовое описание 2"
        )

        self.account_manager.add_transaction(test_transaction1)
        self.account_manager.add_transaction(test_transaction2)

        new_transaction_data = ["2024-05-03", "Расход", 700, "Новое описание"]
        self.account_manager.edit_transaction(1, new_transaction_data)

        transactions = self.account_manager.load_transactions()

        self.assertEqual(len(transactions), 2)

        edited_transaction = transactions[0]
        self.assertEqual(edited_transaction[0], "2024-05-03")
        self.assertEqual(edited_transaction[1], "Расход")
        self.assertEqual(int(edited_transaction[2]), 700)
        self.assertEqual(edited_transaction[3], "Новое описание")


if __name__ == "__main__":
    unittest.main()
