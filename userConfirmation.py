from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget
from PyQt5.QtCore import Qt
import sys

def user_confirmation():
    app = QApplication(sys.argv)
    widget = QWidget()
    message_box = QMessageBox(widget)
    message_box.setIcon(QMessageBox.Question)
    message_box.setWindowTitle("Confirmation")
    message_box.setText("Do you want to continue creating this form?")
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    # Set the window flags to stay on top of all windows
    message_box.setWindowFlags(message_box.windowFlags() | Qt.WindowStaysOnTopHint)

    # Style the buttons with a blue color
    message_box.setStyleSheet("""
        QMessageBox QPushButton {
            background-color: #007BFF;
            border: 1px solid #007BFF;
            color: white;
            min-width: 80px;
            min-height: 25px;
        }
        QMessageBox QPushButton:hover {
            background-color: #0056b3;
            border: 1px solid #0056b3;
        }
        QMessageBox QPushButton:pressed {
            background-color: #004085;
            border: 1px solid #004085;
        }
    """)

    answer = message_box.exec()
    return answer == QMessageBox.Yes

def main():
    return user_confirmation()

if __name__ == "__main__":
    main()
