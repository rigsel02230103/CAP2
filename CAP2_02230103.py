import os
import random
import string

# File to store account information
ACCOUNTS_FILE = "accounts.txt"


class Account:
    def __init__(self, account_id, pin, account_category, initial_balance=0):
        self.account_id = account_id
        self.pin = pin
        self.account_category = account_category
        self.current_balance = initial_balance

    def add_funds(self, amount):
        self.current_balance += amount
        print(f"Added {amount}. Current balance is {self.current_balance}.")

    def subtract_funds(self, amount):
        if amount > self.current_balance:
            print("Insufficient funds.")
        else:
            self.current_balance -= amount
            print(f"Withdrew {amount}. Current balance is {self.current_balance}.")

    def get_account_details(self):
        return f"{self.account_id},{self.pin},{self.account_category},{self.current_balance}"


class PersonalAccount(Account):
    def __init__(self, account_id, pin, initial_balance=0):
        super().__init__(account_id, pin, "Personal", initial_balance)


class BusinessAccount(Account):
    def __init__(self, account_id, pin, initial_balance=0):
        super().__init__(account_id, pin, "Business", initial_balance)


class BankingSystem:
    def __init__(self):
        self.load_existing_accounts()

    def load_existing_accounts(self):
        self.all_accounts = {}
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r') as file:
                for line in file:
                    account_id, pin, account_type, balance = line.strip().split(',')
                    balance = float(balance)
                    if account_type == "Personal":
                        account = PersonalAccount(account_id, pin, balance)
                    else:
                        account = BusinessAccount(account_id, pin, balance)
                    self.all_accounts[account_id] = account

    def save_all_accounts(self):
        with open(ACCOUNTS_FILE, 'w') as file:
            for account in self.all_accounts.values():
                file.write(account.get_account_details() + "\n")

    def initiate_new_account(self, account_type):
        account_id = ''.join(random.choices(string.digits, k=10))
        pin = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if account_type == "Personal":
            account = PersonalAccount(account_id, pin)
        else:
            account = BusinessAccount(account_id, pin)
        self.all_accounts[account_id] = account
        self.save_all_accounts()
        print(f"New account initiated. Account ID: {account_id}, PIN: {pin}")

    def authenticate_user(self, account_id, pin):
        account = self.all_accounts.get(account_id)
        if account and account.pin == pin:
            print("Authentication successful.")
            return account
        else:
            print("Invalid credentials.")
            return None

    def remove_account(self, account_id):
        if account_id in self.all_accounts:
            del self.all_accounts[account_id]
            self.save_all_accounts()
            print("Account removed.")
        else:
            print("Account not found.")

    def process_transfer(self, sender_account, recipient_id, amount):
        recipient_account = self.all_accounts.get(recipient_id)
        if not recipient_account:
            print("Recipient account not found.")
            return
        if sender_account.current_balance < amount:
            print("Insufficient funds.")
            return
        sender_account.subtract_funds(amount)
        recipient_account.add_funds(amount)
        self.save_all_accounts()
        print(f"Transferred {amount} to account {recipient_id}.")


def start_banking_operations():
    banking_system = BankingSystem()
    while True:
        print("\nBanking System Menu:")
        print("1. Initiate Personal Account")
        print("2. Initiate Business Account")
        print("3. Authenticate User")
        print("4. Exit")
        selection = input("Select an option: ")

        if selection == '1':
            banking_system.initiate_new_account("Personal")
        elif selection == '2':
            banking_system.initiate_new_account("Business")
        elif selection == '3':
            account_id = input("Enter account ID: ")
            pin = input("Enter PIN: ")
            account = banking_system.authenticate_user(account_id, pin)
            if account:
                while True:
                    print("\nUser Account Options:")
                    print("1. Add Funds")
                    print("2. Subtract Funds")
                    print("3. Process Transfer")
                    print("4. Remove Account")
                    print("5. Log Out")
                    user_option = input("Choose an action: ")

                    if user_option == '1':
                        amount = float(input("Enter amount to add: "))
                        account.add_funds(amount)
                        banking_system.save_all_accounts()
                    elif user_option == '2':
                        amount = float(input("Enter amount to subtract: "))
                        account.subtract_funds(amount)
                        banking_system.save_all_accounts()
                    elif user_option == '3':
                        recipient_id = input("Enter recipient account ID: ")
                        amount = float(input("Enter amount to transfer: "))
                        banking_system.process_transfer(account, recipient_id, amount)
                    elif user_option == '4':
                        banking_system.remove_account(account.account_id)
                        break
                    elif user_option == '5':
                        print("Logging out.")
                        break
                    else:
                        print("Invalid option. Please try again.")
        elif selection == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    start_banking_operations()
