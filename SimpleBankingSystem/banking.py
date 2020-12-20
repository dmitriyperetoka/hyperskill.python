import random
import sqlite3


class LuhnAlgorithm:
    @staticmethod
    def get_reminder(card_number_without_checksum):
        digits_sum = 0

        for index, element in enumerate(card_number_without_checksum[::-1]):
            digit = int(element)

            if digit and not index % 2:
                digit = (digit * 2) % 9 or 9

            digits_sum += digit

        return digits_sum % 10

    @classmethod
    def make_checksum(cls, card_number_without_checksum):
        reminder = cls.get_reminder(card_number_without_checksum)

        if reminder:
            return str(10 - reminder)

        return "0"

    @classmethod
    def check_card_number(cls, card_number):
        return cls.make_checksum(card_number[:-1]) == card_number[-1]


class SimpleBankingSystem:
    def __init__(
            self,
            card_issuer_id,
            account_id_length=9,
            pin_length=4,
            database_file_name="card.s3db"
    ):
        self.card_issuer_id = card_issuer_id
        self.account_id_length = account_id_length
        self.pin_length = pin_length
        self.database_file_name = database_file_name
        self.logged_account = None
        self.conn = None
        self.cur = None
        self.menu = {
            "main": {
                "1": (self.create_account, "Create an account"),
                "2": (self.login_account, "Log into account"),
            },
            "account": {
                "1": (self.show_balance, "Balance"),
                "2": (self.add_income, "Add income"),
                "3": (self.do_transfer, "Do transfer"),
                "4": (self.close_account, "Close account"),
                "5": (self.logout_account, "Log out"),
                "6": (self.withdraw, "Withdraw"),
            },
        }
        self.selected_menu_area = "main"

    def create_table_if_not_exists(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS card ("
            "id INTEGER PRIMARY KEY, "
            "number TEXT, "
            "pin TEXT, "
            "balance INTEGER DEFAULT 0"
            ");"
        )

    def make_account_id(self):
        account_id = ""

        while True:
            for _ in range(self.account_id_length):
                account_id += str(random.randint(0, 9))

            lookup_start = len(self.card_issuer_id) + 1
            lookup_length = self.account_id_length

            if self.cur.execute(
                    "SELECT COUNT() FROM card "
                    "WHERE SUBSTR(number, ?, ?) = ?;",
                    (lookup_start, lookup_length, account_id)
            ).fetchone()[0]:
                account_id = ""
                continue

            break

        return account_id

    def make_card_number(self):
        account_id = self.make_account_id()
        checksum = LuhnAlgorithm.make_checksum(
            self.card_issuer_id + account_id
        )
        return self.card_issuer_id + account_id + checksum

    def make_pin(self):
        pin = ""

        for _ in range(self.pin_length):
            pin += str(random.randint(0, 9))

        return pin

    def create_account(self):
        card_number = self.make_card_number()
        pin = self.make_pin()
        self.cur.execute(
            "INSERT INTO card (number, pin) VALUES (?, ?);",
            (card_number, pin)
        )
        self.conn.commit()
        print(
            "Your card has been created\n"
            "Your card number:\n"
            f"{card_number}\n"
            "Your card PIN:\n"
            f"{pin}\n"
        )

    def login_account(self):
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        pin = input()
        account_selection = self.cur.execute(
            "SELECT number FROM card WHERE number = ? AND pin = ?;",
            (card_number, pin)
        ).fetchone()

        if not account_selection:
            return print("\nWrong card number or PIN!\n")

        self.logged_account = account_selection[0]
        self.selected_menu_area = "account"
        print("\nYou have successfully logged in!\n")

    def get_balance(self):
        return self.cur.execute(
            "SELECT balance FROM card WHERE number = ?;",
            (self.logged_account,)
        ).fetchone()[0]

    def show_balance(self):
        balance = self.get_balance()
        print(f"Balance: {balance}\n")

    def change_balance(self, operator, amount, account):
        self.cur.execute(
            f"UPDATE card SET balance = balance {operator} ? "
            "WHERE number = ?;",
            (amount, account)
        )

    def check_amount_warnings(self, amount, check_balance=True):
        if amount <= 0:
            print("The amount must be a natural number!\n")
            return True

        if check_balance and amount > self.get_balance():
            print("Not enough money!\n")
            return True

    def check_card_number_warnings(self, destination_card_number):
        if not LuhnAlgorithm.check_card_number(destination_card_number):
            print(
                "Probably you made a mistake in the card number. "
                "Please try again!\n"
            )
            return True

        if not self.cur.execute(
                "SELECT COUNT() FROM card "
                "WHERE number = ?;",
                (destination_card_number,)
        ).fetchone()[0]:
            print("\nSuch a card does not exist.\n")
            return True

    def add_income(self):
        print("Enter income:")
        amount = int(input())

        if self.check_amount_warnings(amount, check_balance=False):
            return

        self.change_balance("+", amount, self.logged_account)
        self.conn.commit()
        print("Income was added!\n")

    def do_transfer(self):
        print("Transfer\nEnter card number:")
        destination_card_number = input()

        if self.check_card_number_warnings(destination_card_number):
            return

        print("Enter how much money you want to transfer:")
        amount = int(input())

        if self.check_amount_warnings(amount):
            return

        self.change_balance("-", amount, self.logged_account)
        self.change_balance("+", amount, destination_card_number)
        self.conn.commit()
        print("Success!\n")

    def close_account(self):
        balance = self.get_balance()

        if balance != 0:
            return print(
                "Only empty accounts can be closed! "
                f"Your balance is {balance}.\n"
                "Please transfer or withdraw all the money and try again.\n"
            )

        self.cur.execute(
            "DELETE FROM card WHERE number = ?",
            (self.logged_account,)
        )
        self.conn.commit()
        self.logged_account = None
        self.selected_menu_area = "main"
        print("The account is successfully closed!\n")

    def logout_account(self):
        self.logged_account = None
        self.selected_menu_area = "main"
        print("You have successfully logged out!\n")

    def withdraw(self):
        print("Enter how much money you want to withdraw:")
        amount = int(input())
        balance = self.get_balance()

        if amount > balance:
            return print("Not enough money!\n")

        if amount <= 0:
            return print("The amount must be a natural number!\n")

        self.change_balance("-", amount, self.logged_account)
        self.conn.commit()
        print("Success!\n")

    def show_menu(self):
        for item in self.menu[self.selected_menu_area]:
            print(f"{item}. {self.menu[self.selected_menu_area][item][1]}")
        print("0. Exit\n")

    def run(self):
        self.conn = sqlite3.connect(self.database_file_name)
        self.cur = self.conn.cursor()
        self.create_table_if_not_exists()

        while True:
            self.show_menu()
            command = input()
            print()

            if command == "0":
                self.conn.close()
                self.conn, self.cur = None, None
                print("Bye!")
                break
            elif command in self.menu[self.selected_menu_area]:
                try:
                    self.menu[self.selected_menu_area][command][0].__call__()
                except ValueError:
                    print("Unexpected input format!\n")
                    continue
            else:
                print("Unknown command!\n")


def main():
    simple_banking_system = SimpleBankingSystem("400000")
    simple_banking_system.run()


if __name__ == "__main__":
    main()
