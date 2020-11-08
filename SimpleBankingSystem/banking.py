import random
import sqlite3


class LuhnAlgorithm:
    @classmethod
    def get_reminder(cls, card_number_without_checksum):
        digits = [int(q) for q in card_number_without_checksum[::-1]]

        for number, digit in enumerate(digits):
            if not number % 2:
                digit *= 2
                if digit > 9:
                    digit -= 9
                digits[number] = digit

        return sum(digits) % 10

    @classmethod
    def make_checksum(cls, card_number_without_checksum):
        reminder = cls.get_reminder(card_number_without_checksum)

        if reminder:
            return str(10 - reminder)

        return "0"

    @classmethod
    def check_card_number(cls, card_number):
        return not (
            (cls.get_reminder(card_number[:-1]) + int(card_number[-1])) % 10
        )


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
        self.selected_menu_area = None
        self.logged_account = None
        self.conn = sqlite3.connect(database_file_name)
        self.cur = self.conn.cursor()

    def create_table_if_not_exists(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS card ("
            "id INTEGER PRIMARY KEY, "
            "number TEXT, "
            "pin TEXT, "
            "balance INTEGER DEFAULT 0"
            ");"
        )

    def make_account_id_number(self):
        account_id_number = ""

        while True:
            for _ in range(self.account_id_length):
                account_id_number += str(random.randint(0, 9))

            lookup_start = len(self.card_issuer_id) + 1
            lookup_length = self.account_id_length

            if self.cur.execute(
                    "SELECT COUNT() FROM card "
                    "WHERE SUBSTR(number, ?, ?) = ?;",
                    (lookup_start, lookup_length, account_id_number,)
            ).fetchone()[0]:
                account_id_number = ""
                continue

            break

        return account_id_number

    def make_pin(self):
        pin = ""
        for _ in range(self.pin_length):
            pin += str(random.randint(0, 9))
        return pin

    def create_account(self):
        card_number = self.card_issuer_id + self.make_account_id_number()
        card_number += LuhnAlgorithm.make_checksum(card_number)
        pin = self.make_pin()
        self.cur.execute(
            "INSERT INTO card (number, pin) VALUES (?, ?);",
            (card_number, pin)
        )
        self.conn.commit()
        print(
            "\nYour card has been created\n"
            "Your card number:\n"
            f"{card_number}\n"
            "Your card PIN:\n"
            f"{pin}\n"
        )

    def login_account(self):
        print("\nEnter your card number:")
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

    def change_balance(self, operator, amount, account):
        self.cur.execute(
            f"UPDATE card SET balance = balance {operator} ? "
            "WHERE number = ?;",
            (amount, account)
        )

    def show_balance(self):
        balance = self.get_balance()
        print(f"\nBalance: {balance}\n")

    def add_income(self):
        print("\nEnter income:")
        income = int(input())
        self.change_balance("+", income, self.logged_account)
        self.conn.commit()
        print("Income was added!\n")

    def do_transfer(self):
        print("\nTransfer\nEnter card number:")
        destination_card_number = input()

        if not LuhnAlgorithm.check_card_number(destination_card_number):
            return print(
                "Probably you made a mistake in the card number. "
                "Please try again!\n"
            )

        if not self.cur.execute(
                "SELECT COUNT() FROM card "
                "WHERE number = ?;",
                (destination_card_number,)
        ).fetchone()[0]:
            return print("\nSuch a card does not exist.\n")

        print("Enter how much money you want to transfer:")
        amount = int(input())
        balance = self.get_balance()

        if amount > balance:
            return print("Not enough money!\n")

        self.change_balance("-", amount, self.logged_account)
        self.change_balance("+", amount, destination_card_number)
        self.conn.commit()
        print("Success!\n")

    def close_account(self):
        balance = self.get_balance()

        if balance != 0:
            return print(
                "\nOnly empty accounts can be closed! "
                f"Your balance is {balance}.\n"
                "Please transfer or withdraw all the money and try again.\n"
            )

        self.cur.execute(
            "DELETE FROM card WHERE number = ?",
            (self.logged_account,)
        )
        self.conn.commit()
        self.logged_account = None
        self.selected_menu_area = None
        print("\nThe account is successfully closed!\n")

    def logout_account(self):
        self.logged_account = None
        self.selected_menu_area = None
        print("\nYou have successfully logged out!\n")

    def withdraw(self):
        print("\nWithdraw\nEnter how much money you want to withdraw:")
        amount = int(input())
        balance = self.get_balance()

        if amount > balance:
            return print("Not enough money!\n")

        self.change_balance("-", amount, self.logged_account)
        self.conn.commit()
        print("Success!\n")

    @property
    def menu(self):
        if self.selected_menu_area == "account":
            return {
                "1": (self.show_balance, "Balance"),
                "2": (self.add_income, "Add income"),
                "3": (self.do_transfer, "Do transfer"),
                "4": (self.close_account, "Close account"),
                "5": (self.logout_account, "Log out"),
                "6": (self.withdraw, "Withdraw")
            }
        else:
            return {
                "1": (self.create_account, "Create an account"),
                "2": (self.login_account, "Log into account"),
            }

    def show_menu(self):
        for q in self.menu:
            print(f"{q}. {self.menu[q][1]}")
        print("0. Exit")

    def run(self):
        self.create_table_if_not_exists()

        while True:
            self.show_menu()
            command = input()

            if command == "0":
                break
            elif command in self.menu:
                try:
                    self.menu[command][0].__call__()
                except ValueError:
                    print("\nUnexpected input format!\n")
                    continue
            else:
                print("\nUnknown command!\n")


def main():
    simple_banking_system = SimpleBankingSystem("400000")
    simple_banking_system.run()


if __name__ == "__main__":
    main()
