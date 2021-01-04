import random
import sqlite3


class LuhnAlgorithm:
    """Toolkit for calculating and validating checksum of bank card
    number based on Luhn algorithm.
    """

    @staticmethod
    def calculate_checksum(digits_before_checksum: str) -> str:
        """ Calculate checksum with the help of applying Luhn formula
        on the digits before checksum.
        """
        digits_sum = 0

        for index, element in enumerate(digits_before_checksum[::-1]):
            digit = int(element)

            if digit and not index % 2:
                digit = (digit * 2) % 9 or 9

            digits_sum += digit

        reminder = digits_sum % 10

        if reminder:
            return str(10 - reminder)

        return "0"

    @classmethod
    def validate_checksum(cls, card_number: str) -> bool:
        """Calculate checksum and compare it with the provided one."""
        return cls.calculate_checksum(card_number[:-1]) == card_number[-1]


class SimpleBankingSystem:
    """Simple banking system with database that can store accounts
    and transactions.
    """

    def __init__(
            self,
            card_issuer_id: str,
            account_id_length: int = 9,
            pin_length: int = 4,
            database_file_name: str = "card.s3db"
    ) -> None:
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
                "1": (self.print_balance, "Balance"),
                "2": (self.add_income, "Add income"),
                "3": (self.do_transfer, "Do transfer"),
                "4": (self.close_account, "Close account"),
                "5": (self.logout_account, "Log out"),
                "6": (self.withdraw, "Withdraw"),
            },
        }
        self.selected_menu_area = "main"

    def create_account_id(self) -> str:
        """Create account ID as a random unique numeric sequence."""
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

    def create_card_number(self) -> str:
        """Create card number as concatenation of predefined issuer ID
         with created account ID and calculated checksum.
        """
        account_id = self.create_account_id()
        checksum = LuhnAlgorithm.calculate_checksum(
            self.card_issuer_id + account_id
        )
        return self.card_issuer_id + account_id + checksum

    def create_pin(self) -> str:
        """Create PIN as a random numeric sequence."""
        pin = ""

        for _ in range(self.pin_length):
            pin += str(random.randint(0, 9))

        return pin

    def create_account(self) -> None:
        """Create card number and PIN and save them to the database."""
        card_number = self.create_card_number()
        pin = self.create_pin()
        self.cur.execute(
            "INSERT INTO card (number, pin) VALUES (?, ?);",
            (card_number, pin)
        )
        self.conn.commit()
        print(
            "Your card has been created.\n"
            "Your card number:\n"
            f"{card_number}\n"
            "Your card PIN:\n"
            f"{pin}"
        )

    def validate_login_data(self, card_number: str, pin: str) -> bool:
        """Validate card number and PIN."""
        return (
            len(card_number)
            == len(self.card_issuer_id) + self.account_id_length + 1
            and len(pin) == self.pin_length
            and card_number.isdigit()
            and pin.isdigit()
            and LuhnAlgorithm.validate_checksum(card_number)
            and self.cur.execute(
                "SELECT COUNT() FROM card WHERE number = ? AND pin = ?;",
                (card_number, pin)
            ).fetchone()[0]
        )

    def login_account(self) -> None:
        """Log into account if provided login data is valid."""
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        pin = input()
        print()

        if not self.validate_login_data(card_number, pin):
            return print("Wrong card number or PIN!")

        self.logged_account = card_number
        self.selected_menu_area = "account"
        print("You have successfully logged in!")

    def get_balance(self) -> int:
        """Return balance of the account that is currently logged in."""
        return self.cur.execute(
            "SELECT balance FROM card WHERE number = ?;",
            (self.logged_account,)
        ).fetchone()[0]

    def print_balance(self) -> None:
        """Print balance of the account that is currently logged in."""
        balance = self.get_balance()
        print(f"Balance: {balance}")

    def validate_amount(self, amount: int, check_balance: bool = True) -> bool:
        """Validate specified amount before changing balance."""
        if amount <= 0:
            print("The amount must be a natural number!")
            return False

        if check_balance and amount > self.get_balance():
            print("Not enough money!")
            return False

        return True

    def change_balance(self, operator: str, amount: int, account: str) -> None:
        """Change balance of specified account by specified amount."""
        self.cur.execute(
            f"UPDATE card SET balance = balance {operator} ? "
            "WHERE number = ?;",
            (amount, account)
        )

    def add_income(self) -> None:
        """Add income to the account that is currently logged in."""
        print("Enter income:")
        amount = int(input())

        if not self.validate_amount(amount, check_balance=False):
            return

        self.change_balance("+", amount, self.logged_account)
        self.conn.commit()
        print("Income was added!")

    def validate_card_number(self, card_number: str) -> bool:
        """Validate destination card number before doing transfer."""
        if not LuhnAlgorithm.validate_checksum(card_number):
            print(
                "Probably you made a mistake in the card number. "
                "Please try again!"
            )

            return False

        if not self.cur.execute(
                "SELECT COUNT() FROM card WHERE number = ?;", (card_number,)
        ).fetchone()[0]:
            print("Such a card does not exist.")

            return False

        if card_number == self.logged_account:
            print("Can not transfer to your own account!")

            return False

        return True

    def do_transfer(self) -> None:
        """Transfer specified account to specified amount."""
        print("Transfer")
        print("Enter card number:")
        destination_card_number = input()

        if not self.validate_card_number(destination_card_number):
            return

        print("Enter how much money you want to transfer:")
        amount = int(input())

        if not self.validate_amount(amount):
            return

        self.change_balance("-", amount, self.logged_account)
        self.change_balance("+", amount, destination_card_number)
        self.conn.commit()
        print("Success!")

    def close_account(self) -> None:
        """Close the account that is currently logged in."""
        balance = self.get_balance()

        if balance != 0:
            return print(
                "Only empty accounts can be closed! "
                f"Your balance is {balance}.\n"
                "Please transfer or withdraw all the money and try again."
            )

        self.cur.execute(
            "DELETE FROM card WHERE number = ?",
            (self.logged_account,)
        )
        self.conn.commit()
        self.logged_account = None
        self.selected_menu_area = "main"
        print("The account is successfully closed!")

    def logout_account(self) -> None:
        """Logout from the account that is currently logged in."""
        self.logged_account = None
        self.selected_menu_area = "main"
        print("You have successfully logged out!")

    def withdraw(self) -> None:
        """Withdraw from the account that is currently logged in."""
        print("Enter how much money you want to withdraw:")
        amount = int(input())

        if not self.validate_amount(amount):
            return

        self.change_balance("-", amount, self.logged_account)
        self.conn.commit()
        print("Success!")

    def setup(self) -> None:
        """Create database if it does not exist. Create DB connection.
        Create main table if it does not exist in the database."""
        self.conn = sqlite3.connect(self.database_file_name)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS card ("
            "id INTEGER PRIMARY KEY, "
            "number TEXT, "
            "pin TEXT, "
            "balance INTEGER DEFAULT 0"
            ");"
        )

    def print_menu(self) -> None:
        """Print the options of the currently selected menu area."""
        for item in self.menu[self.selected_menu_area]:
            print(f"{item}. {self.menu[self.selected_menu_area][item][1]}")
        print("0. Exit")

    def run(self) -> None:
        """Run the main loop of the program."""
        self.setup()

        while True:
            self.print_menu()
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
                    print("Unexpected input format!")
            else:
                print("Unknown command!")

            print()


def main() -> None:
    """Initialize the program."""
    simple_banking_system = SimpleBankingSystem("400000")
    simple_banking_system.run()


if __name__ == "__main__":
    main()
