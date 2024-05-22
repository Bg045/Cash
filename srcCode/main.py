import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt5 import QtGui, QtCore

class Admin:
    accounts = []

    def __init__(self, login, password, number, pin, balance=0):
        self.login = login
        self.password = password
        self.number = number
        self.pin = pin
        self.balance = balance
        Admin.accounts.append(self)

class Client:
    accounts = []

    def __init__(self, login, password, number, pin, balance=0):
        self.login = login
        self.password = password
        self.number = number
        self.pin = pin
        self.balance = balance
        Client.accounts.append(self)

class ChargingWindow(QWidget):
    def __init__(self, admin_accounts, client_accounts):
        super().__init__()

        self.admin_accounts = admin_accounts
        self.client_accounts = client_accounts

        self.setWindowTitle("Charging")
        self.setGeometry(200, 200, 400, 200)
        self.setStyleSheet("QWidget { background-color: #333333; color: white; }")

        layout = QVBoxLayout(self)

        charging_label = QLabel("Charging Window")
        charging_label.setStyleSheet("font-size: 18px; color: white; margin-bottom: 10px;")
        layout.addWidget(charging_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Enter Login or Card Number")
        layout.addWidget(self.login_input)

        self.sum_input = QLineEdit()
        self.sum_input.setPlaceholderText("Enter Sum")
        layout.addWidget(self.sum_input)

        charge_button = QPushButton("Charge")
        charge_button.setStyleSheet("padding: 7px; background-color: #1E90FF; color: white; border: none; border-radius: 5px;")
        charge_button.clicked.connect(self.charge)
        layout.addWidget(charge_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("padding: 5px; background-color: #FF6347; color: white; border: none; border-radius: 5px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    def charge(self):
        login = self.login_input.text()
        sum = float(self.sum_input.text())

        user_found = False
        for admin in self.admin_accounts:
            if admin.login == login:
                admin.balance += sum
                user_found = True
                print(f"Charging {sum} for login: {login}")
                break

        if not user_found:
            for client in self.client_accounts:
                if client.login == login:
                    client.balance += sum
                    user_found = True
                    print(f"Charging {sum} for login: {login}")
                    break

        if not user_found:
            print("User not found. Please enter a valid login or card number.")

class CashingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cashing")
        self.setGeometry(200, 200, 400, 200)
        self.setStyleSheet("QWidget { background-color: #333333; color: white; }")

        layout = QVBoxLayout(self)

        cashing_label = QLabel("Cashing Window")
        cashing_label.setStyleSheet("font-size: 18px; color: white; margin-bottom: 10px;")
        layout.addWidget(cashing_label)

        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Enter Card Number")
        layout.addWidget(self.card_number_input)

        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("Enter PIN")
        layout.addWidget(self.pin_input)

        self.sum_input = QLineEdit()
        self.sum_input.setPlaceholderText("Enter Sum")
        layout.addWidget(self.sum_input)

        cash_button = QPushButton("Cash")
        cash_button.setStyleSheet("padding: 7px; background-color: #1E90FF; color: white; border: none; border-radius: 5px;")
        cash_button.clicked.connect(self.cash)
        layout.addWidget(cash_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("padding: 5px; background-color: #FF6347; color: white; border: none; border-radius: 5px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    def cash(self):
        card_number = self.card_number_input.text()
        pin = self.pin_input.text()
        cash_sum = float(self.sum_input.text())

        for admin in Admin.accounts:
            if admin.number == card_number and admin.pin == pin:
                if admin.balance >= cash_sum:
                    admin.balance -= cash_sum
                    print(f"Withdrawn {cash_sum} from account with card number: {card_number}")
                else:
                    print("Insufficient funds")
                return

        for client in Client.accounts:
            if client.number == card_number and client.pin == pin:
                if client.balance >= cash_sum:
                    client.balance -= cash_sum
                    print(f"Withdrawn {cash_sum} from account with card number: {card_number}")
                else:
                    print("Insufficient funds")
                return

        print("User not found or invalid PIN")

class BalanceCheckingWindow(QWidget):
    def __init__(self, admin_accounts=None, client_accounts=None):
        super().__init__()

        self.admin_accounts = admin_accounts if admin_accounts else []
        self.client_accounts = client_accounts if client_accounts else []

        self.setWindowTitle("Balance Checking")
        self.setGeometry(200, 200, 400, 200)
        self.setStyleSheet("QWidget { background-color: #333333; color: white; }")

        layout = QVBoxLayout(self)

        balance_label = QLabel("Balance Checking Window")
        balance_label.setStyleSheet("font-size: 18px; color: white; margin-bottom: 10px;")
        layout.addWidget(balance_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Enter Login")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        check_balance_button = QPushButton("Check Balance")
        check_balance_button.setStyleSheet("padding: 7px; background-color: #1E90FF; color: white; border: none; border-radius: 5px;")
        check_balance_button.clicked.connect(self.check_balance)
        layout.addWidget(check_balance_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("padding: 5px; background-color: #FF6347; color: white; border: none; border-radius: 5px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    def check_balance(self):
        login = self.login_input.text()
        password = self.password_input.text()

        user_found = False
        for admin in self.admin_accounts:
            if admin.login == login and admin.password == password:
                print(f"Admin Balance: {admin.balance}")
                user_found = True
                break

        if not user_found:
            for client in self.client_accounts:
                if client.login == login and client.password == password:
                    print(f"Client Balance: {client.balance}")
                    user_found = True
                    break

        if not user_found:
            print("User not found or invalid credentials.")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 500, 150)
        self.setStyleSheet("QWidget { background-color: #333333; color: white; }")

        splitter = QSplitter()
        self.left_widget = QWidget()
        self.right_widget = QWidget()

        splitter.addWidget(self.left_widget)
        splitter.addWidget(self.right_widget)

        self.setup_left_widget()
        self.setup_right_widget()

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.right_widget.hide()

    def setup_left_widget(self):
        layout = QVBoxLayout(self.left_widget)

        charging_button = QPushButton("Charging")
        charging_button.setMinimumWidth(200)
        charging_button.setMinimumHeight(30)
        charging_button.setStyleSheet("QPushButton { background-color: #292929; color: white; border: none; border-radius: 5px; }"
                                      "QPushButton:hover { background-color: #1E90FF; }"
                                      "QPushButton:pressed { background-color: #0F52BA; }")
        charging_button.clicked.connect(self.show_charging_window)
        layout.addWidget(charging_button)

        cashing_button = QPushButton("Cashing")
        cashing_button.setMinimumWidth(200)
        cashing_button.setMinimumHeight(30)
        cashing_button.setStyleSheet("QPushButton { background-color: #292929; color: white; border: none; border-radius: 5px; }"
                                     "QPushButton:hover { background-color: #1E90FF; }"
                                     "QPushButton:pressed { background-color: #0F52BA; }")
        cashing_button.clicked.connect(self.show_cashing_window)
        layout.addWidget(cashing_button)

        balance_checking_button = QPushButton("Balance Checking")
        balance_checking_button.setMinimumWidth(200)
        balance_checking_button.setMinimumHeight(30)
        balance_checking_button.setStyleSheet("QPushButton { background-color: #292929; color: white; border: none; border-radius: 5px; }"
                                              "QPushButton:hover { background-color: #1E90FF; }"
                                              "QPushButton:pressed { background-color: #0F52BA; }")
        balance_checking_button.clicked.connect(self.show_balance_checking_window)
        layout.addWidget(balance_checking_button)

        login_label = QLabel("Log In Admin")
        login_label.setStyleSheet("font-size: 18px; color: white; margin-bottom: 10px;")
        layout.addWidget(login_label)

        self.admin_username_label = QLabel("Admin Username:")
        self.admin_username_input = QLineEdit()
        self.admin_username_input.setStyleSheet("padding: 5px; background-color: #444444; color: white; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.admin_username_label)
        layout.addWidget(self.admin_username_input)

        self.admin_password_label = QLabel("Admin Password:")
        self.admin_password_input = QLineEdit()
        self.admin_password_input.setEchoMode(QLineEdit.Password)
        self.admin_password_input.setStyleSheet("padding: 5px; background-color: #444444; color: white; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.admin_password_label)
        layout.addWidget(self.admin_password_input)

        self.login_button = QPushButton("Log In Admin")
        self.login_button.setMinimumWidth(200)
        self.login_button.setStyleSheet("padding: 7px; background-color: #1E90FF; color: white; border: none; border-radius: 5px;")
        self.login_button.clicked.connect(self.log_in_admin)
        layout.addWidget(self.login_button)

        self.client_username_label = QLabel("Client Username:")
        self.client_username_input = QLineEdit()
        self.client_username_input.setStyleSheet("padding: 5px; background-color: #444444; color: white; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.client_username_label)
        layout.addWidget(self.client_username_input)

        self.client_password_label = QLabel("Client Password:")
        self.client_password_input = QLineEdit()
        self.client_password_input.setEchoMode(QLineEdit.Password)
        self.client_password_input.setStyleSheet("padding: 5px; background-color: #444444; color: white; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.client_password_label)
        layout.addWidget(self.client_password_input)

        self.login_button_client = QPushButton("Log In Client")
        self.login_button_client.setMinimumWidth(200)
        self.login_button_client.setStyleSheet("padding: 7px; background-color: #1E90FF; color: white; border: none; border-radius: 5px;")
        self.login_button_client.clicked.connect(self.log_in_client)
        layout.addWidget(self.login_button_client)

    def setup_right_widget(self):
        layout = QVBoxLayout(self.right_widget)

        header_layout = QHBoxLayout()
        bank_card_label = QLabel("Bank Card Generation")
        bank_card_label.setStyleSheet("font-size: 18px; color: white; margin-bottom: 10px;")
        header_layout.addWidget(bank_card_label)
        close_button = QPushButton("X")
        close_button.setStyleSheet("padding: 5px; background-color: #FF6347; color: white; border: none; border-radius: 5px;")
        close_button.clicked.connect(self.close_right_widget)
        header_layout.addWidget(close_button)
        layout.addLayout(header_layout)

        self.account_number_label = QLabel("Account Number:")
        self.account_number_value = QLabel()
        self.generate_bank_account()
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_value)

        self.pin_label = QLabel("PIN:")
        self.pin_value = QLabel()
        self.generate_pin()
        layout.addWidget(self.pin_label)
        layout.addWidget(self.pin_value)

        self.generate_button = QPushButton("Generate New Card")
        self.generate_button.setMinimumWidth(200)
        self.generate_button.setStyleSheet("padding: 7px; background-color: #1E90FF; color: white; border: none; border-radius: 5px;")
        self.generate_button.clicked.connect(self.generate_new_card)
        layout.addWidget(self.generate_button)

    def generate_bank_account(self):
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(16))
        self.account_number_value.setText(account_number)

    def generate_pin(self):
        pin = ''.join(str(random.randint(0, 9)) for _ in range(4))
        self.pin_value.setText(pin)

    def generate_new_card(self):
        self.generate_bank_account()
        self.generate_pin()

    def log_in_admin(self):
        login = self.admin_username_input.text()
        password = self.admin_password_input.text()

        number = self.account_number_value.text()
        pin = self.pin_value.text()
        admin = Admin(login, password, number, pin)
        print("Admin created:", vars(admin))

        self.right_widget.show()

    def log_in_client(self):
        login = self.client_username_input.text()
        password = self.client_password_input.text()

        number = self.account_number_value.text()
        pin = self.pin_value.text()
        client = Client(login, password, number, pin)
        print("Client created:", vars(client))

        self.right_widget.show()

    def close_right_widget(self):
        self.right_widget.hide()

    def show_charging_window(self):
        admin_accounts = Admin.accounts
        client_accounts = Client.accounts

        self.charging_window = ChargingWindow(admin_accounts, client_accounts)
        self.charging_window.show()

    def show_cashing_window(self):
        self.cashing_window = CashingWindow()
        self.cashing_window.show()

    def show_balance_checking_window(self):
        admin_accounts = Admin.accounts
        client_accounts = Client.accounts

        self.balance_checking_window = BalanceCheckingWindow(admin_accounts, client_accounts)
        self.balance_checking_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())


#EXITTTT!!!

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
