import sys
import os
import json
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtGui import QPixmap

KEY_FILE = "encryption_key.key"
CREDENTIALS_FILE = "credentials.enc"


def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return None, None
    with open(CREDENTIALS_FILE, "rb") as f:
        encrypted_data = f.read()
    return json.loads(Fernet(load_key()).decrypt(encrypted_data).decode())


def login_dialog():
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Create a login dialog
    dialog = QDialog()
    dialog.setWindowTitle("Asite Login (Make sure you have API access)")
    dialog.setFixedWidth(1500)
    dialog.setFixedHeight(1500)


    layout = QVBoxLayout()

    # Add the logo label
    logo_label = QLabel()
    logo_pixmap = QPixmap("WBHO.PNG")
    logo_label.setPixmap(logo_pixmap)
    logo_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(logo_label)

    # Set the size of the dialog to match the size of the logo
    dialog.setFixedSize(logo_pixmap.width(), logo_pixmap.height() + 200) # Increase height by 200
    dialog.setFixedWidth(250)

    # Add the text label
    text_label = QLabel("Weekly Dashboard Excel to Asite generator")
    text_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(text_label)

    # # Read the ASCII art logo from the logo.txt file
    # with open("logo.txt", "r", encoding="utf-8") as f:
    #     ascii_logo = f.read()

    #logo_label = QLabel(ascii_logo)
    # logo_label.setAlignment(Qt.AlignCenter)
    # logo_label.setStyleSheet("color: white; font-family: monospace;")
    # layout.addWidget(logo_label)

    # Set the blue theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(42, 130, 218))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(255, 165, 0))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    # Create username and password input fields
    layout.addWidget(QLabel("Asite Username:"))
    username_input = QLineEdit()
    layout.addWidget(username_input)

    layout.addWidget(QLabel("Password:"))
    password_input = QLineEdit()
    password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(password_input)

    # Create a "Remember me" checkbox
    remember_me_checkbox = QCheckBox("Remember me")
    layout.addWidget(remember_me_checkbox)

    # Create a login button
    login_button = QPushButton("Login")
    layout.addWidget(login_button)
    login_button.setFont(QFont("Arial", 10))  # Increase font size to 16




    # Connect the login button to the accept() slot of the dialog
    login_button.clicked.connect(dialog.accept)

    dialog.setLayout(layout)

    # Load saved credentials if available
    saved_username, saved_password = load_credentials()
    if saved_username and saved_password:
        username_input.setText(saved_username)
        password_input.setText(saved_password)
        remember_me_checkbox.setChecked(True)

    # Execute the dialog and retrieve the login information
    result = dialog.exec_()
    username = username_input.text()
    password = password_input.text()
    remember_me = remember_me_checkbox.isChecked()

    # Save the credentials if the user checked "Remember me"
    if remember_me:
        save_credentials(username, password)
    else:
        if os.path.exists(CREDENTIALS_FILE):
            os.remove(CREDENTIALS_FILE)

    if result == QDialog.Accepted:
        return username, password
    else:
        return None, None


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def save_credentials(username, password):
    if not os.path.exists(KEY_FILE):
        generate_key()
    encrypted_data = Fernet(load_key()).encrypt(json.dumps((username, password)).encode())
    with open(CREDENTIALS_FILE, "wb") as f:
        f.write(encrypted_data)

    with open(CREDENTIALS_FILE, "wb") as f:
        f.write(encrypted_data)

if __name__ == "__main__":
    username, password = login_dialog()
    if username and password:
        print(f"Logged in with username: {username} and password: {password}")
    else:
        print("Login canceled")
