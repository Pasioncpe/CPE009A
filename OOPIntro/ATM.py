"""
    ATM.py
"""

class ATM:
    serial_number = 0

    def __init__(self):
        ATM.serial_number += 1
        self.id = ATM.serial_number
        self.transactions = []

    def deposit(self, account, amount):
        account.current_balance = account.current_balance + amount
        self.transactions.append(
            f"Deposit: +{amount} to {account.account_firstname} {account.account_lastname}"
        )
        print("Deposit Complete")

    def widthdraw(self, account, amount):
        account.current_balance = account.current_balance - amount
        self.transactions.append(
            f"Withdraw: -{amount} from {account.account_firstname} {account.account_lastname}"
        )
        print("Widthdraw Complete")

    def check_currentbalance(self, account):
        print(account.current_balance)

    def view_transactionsummary(self):
        print("\nTransaction Summary:")
        if not self.transactions:
            print("No transactions made.")
        else:
            for t in self.transactions:
                print(t)