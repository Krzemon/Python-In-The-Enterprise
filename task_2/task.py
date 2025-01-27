import random
import logging

# custom exceptions
class InsufficientFundsException(Exception):
    def __init__(self, message="Insufficient funds in the account"):
        super().__init__(message)

class InvalidAmountException(Exception):
    def __init__(self, message="The amount must be positive and greater than zero"):
        super().__init__(message)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# decorator
def log_operation(func):
    def wrapper(self, *args, **kwargs):
        logger.info(f"Calling method: {func.__name__} with arguments: {args}, {kwargs}")
        result = func(self, *args, **kwargs) 
        logger.info(f"Finished execution of method: {func.__name__} with result: {result}")
        return result
    return wrapper

class Bank:
    def __init__(self):
        self.accounts = set()

    def add_account(self, account):
        if account.account_number not in {acc.account_number for acc in self.accounts}:
            self.accounts.add(account)

    @staticmethod
    def load_from_file(filename):
        bank = Bank()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    account_number, owner_name, phone, balance = data
                    account = BankAccount(owner_name, phone, float(balance))
                    bank.add_account(account)
        except FileNotFoundError:
            print(f"Plik {filename} not exist.")
        return bank

    @log_operation
    def display_all_accounts(self):
        for account in self.accounts:
            print(account)


class BankAccount:    
    used_account_numbers = set()

    def __init__(self, owner_name, phone, balance):
        self.owner_name = owner_name
        self.phone = phone
        self.balance = balance
        self.account_number = self.generate_account_number()

    @classmethod
    def generate_account_number(cls):
        while True:
            account_number = ''.join(str(random.randint(0, 9)) for _ in range(26))
            iban = (
                f"PL{random.randint(10, 99)} "
                f"{account_number[:4]} "
                f"{account_number[4:8]} "
                f"{account_number[8:12]} "
                f"{account_number[12:16]} "
                f"{account_number[16:20]} "
                f"{account_number[20:24]} "
                f"{account_number[24:26]}")            
            if iban not in cls.used_account_numbers:
                cls.used_account_numbers.add(iban)
                return iban
    
    @log_operation 
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountException("Error: Not enough funds.")
        self.balance += amount
        return f"Deposited {amount}. New balance: {self.balance}"
    
    @log_operation 
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsException("Error: There are not so many resources.")
        if amount <= 0:
            raise InvalidAmountException("Error: Not enough funds.")
        self.balance -= amount
        return f"Withdrew {amount}. New balance: {self.balance}"

    @log_operation 
    def transfer(self, target_account, amount):
        if amount > self.balance:
            raise InsufficientFundsException("Error: There are not so many resources.")
        if amount <= 0:
            raise InvalidAmountException("Error: Not enough funds.")
        self.balance -= amount
        target_account.balance += amount
        return f"Transferred {amount} to account {target_account.account_number}. New balance: {self.balance}"

    def save_to_file(self, filename):
        with open(filename, 'a') as file:
            file.write(f"{self.account_number},{self.owner_name},{self.phone},{self.balance}\n")
    
    def __str__(self):
        return f"Account {self.account_number}, Owner: {self.owner_name}, Balance: {self.balance}, Phone: {self.phone}"


if __name__ == "__main__":
    acc_1 = BankAccount("Adam Nowak", '123456789', 2000)
    acc_2 = BankAccount("Bogdan Swojski", '223456789', 4000000)
    acc_3 = BankAccount("Maria Kwiatkowska", '323456789', 1500)
    acc_4 = BankAccount("Krzysztof Kowal", '423456789', 5000)

    # acc_1.save_to_file('accounts.txt')
    # acc_2.save_to_file('accounts.txt')
    # acc_3.save_to_file('accounts.txt')
    # acc_4.save_to_file('accounts.txt')

    print("\nBefore transfer")
    print(acc_1)
    print(acc_2)

    print(acc_1.deposit(200))
    print(acc_1.withdraw(100))
    print(acc_2.transfer(acc_1, 100000))

    print("\nAfter transfer")

    print(acc_1)
    print(acc_2)

    bank = Bank.load_from_file('accounts.txt')
    
    print("\nAll accounts in bank:")
    bank.display_all_accounts()