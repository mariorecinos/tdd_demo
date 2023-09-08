import csv

class Customer:
    def __init__(self, customer_id, first_name, last_name, email):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.accounts = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Account:
    def __init__(self, account_number, account_type, customer, balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.customer = customer
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

    def transfer(self, recipient_account, amount):
        if self.withdraw(amount):
            recipient_account.deposit(amount)
            return True
        else:
            return False

class Main:
    def __init__(self):
        self.customers = self.load_customers('users.csv')
        self.accounts = self.load_accounts('accounts.csv')

    def load_customers(self, filename):
        customers = []
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    customer = Customer(int(row[0]), row[1], row[2], row[3])
                    customers.append(customer)
        except FileNotFoundError:
            pass
        return customers

    def save_customers(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'First Name', 'Last Name', 'Email'])
            for customer in self.customers:
                writer.writerow([customer.customer_id, customer.first_name, customer.last_name, customer.email])

    def load_accounts(self, filename):
        accounts = []
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    account_number, account_type, customer_id, balance = row
                    customer = next((c for c in self.customers if c.customer_id == int(customer_id)), None)
                    if customer:
                        account = Account(int(account_number), account_type, customer, float(balance))
                        customer.accounts.append(account)
                        accounts.append(account)
        except FileNotFoundError:
            pass
        return accounts

    def save_accounts(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account Number', 'Account Type', 'Customer ID', 'Balance'])
            for account in self.accounts:
                writer.writerow([account.account_number, account.account_type, account.customer.customer_id, account.balance])

    def add_customer(self):
        customer_id = len(self.customers) + 1
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        customer = Customer(customer_id, first_name, last_name, email)
        self.customers.append(customer)
        self.save_customers('users.csv')
        print(f"Customer added with ID {customer_id}")

    def create_account(self):
        customer_id = int(input("Enter customer ID: "))
        account_number = len(self.accounts) + 1
        account_type = input("Enter account type: ")
        initial_balance = float(input("Enter initial balance: "))
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if customer:
            account = Account(account_number, account_type, customer, initial_balance)
            self.accounts.append(account)
            self.save_accounts('accounts.csv')
            print(f"Account created with number {account_number}")
        else:
            print("Customer not found.")

    def deposit_money(self):
        customer_id = int(input("Enter customer ID: "))

        # Find the customer with the given ID
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)

        if customer:
            # Display customer's accounts
            for i, account in enumerate(customer.accounts):
                print(f"{i + 1}. Account {account.account_number} ({account.account_type}): ${account.balance}")

            # Prompt user to select an account to deposit into
            while True:
                account_index = int(input("Select an account (enter the number): ")) - 1
                if 0 <= account_index < len(customer.accounts):
                    selected_account = customer.accounts[account_index]

                    # Prompt user for deposit amount
                    amount = float(input("Enter deposit amount: "))
                    if selected_account.deposit(amount):
                        print(f"Deposited ${amount} into Account {selected_account.account_number}.")
                        break
                    else:
                        print("Invalid deposit amount. Please enter a valid amount.")
                else:
                    print("Invalid account selection. Please enter a valid account number.")
        else:
            print("Customer not found.")

    def withdraw_money(self):
        customer_id = int(input("Enter customer ID: "))

        # Find the customer with the given ID
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)

        if customer:
            # Display customer's accounts
            for i, account in enumerate(customer.accounts):
                print(f"{i + 1}. Account {account.account_number} ({account.account_type}): ${account.balance}")

            # Prompt user to select an account to withdraw from
            while True:
                account_index = int(input("Select an account (enter the number): ")) - 1
                if 0 <= account_index < len(customer.accounts):
                    selected_account = customer.accounts[account_index]

                    # Prompt user for withdrawal amount
                    amount = float(input("Enter withdrawal amount: "))
                    if selected_account.withdraw(amount):
                        print(f"Withdrew ${amount} from Account {selected_account.account_number}.")
                        break
                    else:
                        print("Invalid withdrawal amount. Please enter a valid amount.")
                else:
                    print("Invalid account selection. Please enter a valid account number.")
        else:
            print("Customer not found.")

    def transfer_money(self):
      sender_customer_id = int(input("Enter your customer ID: "))
      recipient_customer_id = int(input("Enter recipient's customer ID: "))

      # Find the sender and recipient customers with the given IDs
      sender_customer = next((c for c in self.customers if c.customer_id == sender_customer_id), None)
      recipient_customer = next((c for c in self.customers if c.customer_id == recipient_customer_id), None)

      if sender_customer and recipient_customer:
        # Display sender's accounts
        print(f"Accounts for {sender_customer}:")
        for i, account in enumerate(sender_customer.accounts):
            print(f"{i + 1}. Account {account.account_number} ({account.account_type}): ${account.balance}")

        # Prompt sender to select an account to transfer from
        while True:
            sender_account_index = int(input("Select an account to transfer from (enter the number): ")) - 1
            if 0 <= sender_account_index < len(sender_customer.accounts):
                sender_account = sender_customer.accounts[sender_account_index]

                # Prompt user for transfer amount
                amount = float(input("Enter transfer amount: "))
                if sender_account.withdraw(amount):
                    # Display recipient's accounts
                    print(f"Accounts for {recipient_customer}:")
                    for i, account in enumerate(recipient_customer.accounts):
                        print(f"{i + 1}. Account {account.account_number} ({account.account_type}): ${account.balance}")

                    # Prompt recipient to select an account to transfer to
                    while True:
                        recipient_account_index = int(input("Select an account to transfer to (enter the number): ")) - 1
                        if 0 <= recipient_account_index < len(recipient_customer.accounts):
                            recipient_account = recipient_customer.accounts[recipient_account_index]
                            if recipient_account.transfer(sender_account, amount):
                                print(f"Transferred ${amount} from Account {sender_account.account_number} to Account {recipient_account.account_number}.")
                                return
                            else:
                                print("Invalid transfer amount. Please enter a valid amount.")
                        else:
                            print("Invalid account selection. Please enter a valid account number.")
                else:
                    print("Invalid withdrawal amount. Please enter a valid amount.")
            else:
                print("Invalid account selection. Please enter a valid account number.")
      else:
        print("Customer not found.")

    def display_transaction_data(self):
        for customer in self.customers:
            print(f"{customer}:")
            for account in customer.accounts:
                print(f"Account {account.account_number} ({account.account_type}): ${account.balance}")

    def main_menu(self):
        while True:
            print("===========================")
            print("\nACME Bank")
            print("1. Add Customer")
            print("2. Create Account")
            print("3. Deposit Money")
            print("4. Withdraw Money")
            print("5. Transfer Money")
            print("6. Display Transaction Data")
            print("7. Exit")
            print("===========================")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_customer()

            elif choice == '2':
                self.create_account()

            elif choice == '3':
                self.deposit_money()

            elif choice == '4':
                self.withdraw_money()

            elif choice == '5':
                self.transfer_money()

            elif choice == '6':
                self.display_transaction_data()

            elif choice == '7':
                print("===========================")
                print("Goodbye Have A Great Day")
                print("===========================")
                break

if __name__ == "__main__":
    bank = Main()
    bank.main_menu()
