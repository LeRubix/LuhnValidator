import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

def luhn_check(card_number):
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

class ResultDialog(QDialog):
    def __init__(self, message, is_valid):
        super().__init__()
        self.setWindowTitle('Result')
        self.setFixedSize(170, 100)
        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)
        self.setLayout(layout)

        if is_valid:
            self.setWindowIcon(QIcon("ui_assets/check.png"))
        else:
            self.setWindowIcon(QIcon("ui_assets/cross.png"))

class WarningDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle('Input Error')
        self.setFixedSize(590, 150)
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)
        self.setLayout(layout)

class HowDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('How does Luhn\'s Algorithm work?')
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()
        
        message = QLabel(
            "Luhn's algorithm is a simple checksum formula used to validate a variety of identification numbers, "
            "such as credit card numbers. For more information, visit: "
            "<a href='https://en.wikipedia.org/wiki/Luhn_algorithm'>Wikipedia</a>"
            " \n "
        )
        
        font = QFont()
        font.setPointSize(12)
        message.setFont(font)
        
        message.setOpenExternalLinks(True)
        message.setWordWrap(True)
        layout.addWidget(message)

        image_label = QLabel()
        pixmap = QPixmap("ui_assets/explain.png")
        image_label.setPixmap(pixmap.scaled(QSize(550, 657), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(image_label)

        self.setLayout(layout)

class CardValidatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Card Validator')
        self.setMinimumSize(400, 200)
        layout = QVBoxLayout()

        self.label = QLabel('Enter Card Number:')
        self.card_input = QLineEdit()
        self.validate_button = QPushButton('Validate')
        self.how_button = QPushButton('How does it work?')

        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.card_input.setFont(font)
        self.validate_button.setFont(font)
        self.how_button.setFont(font)

        self.validate_button.clicked.connect(self.validate_card)
        self.how_button.clicked.connect(self.show_how)

        layout.addWidget(self.label)
        layout.addWidget(self.card_input)
        layout.addWidget(self.validate_button)
        layout.addWidget(self.how_button)

        self.setLayout(layout)

    def validate_card(self):
        card_number = self.card_input.text().strip()
        
        if len(card_number) < 16 or len(card_number) > 19 or not card_number.isdigit():
            warning_message = 'Card number must be between 16 and 19 digits long and contain only numbers.'
            warning_dialog = WarningDialog(warning_message)
            warning_dialog.exec()
            return
        
        is_valid = luhn_check(card_number)
        message = 'Valid Card Number! :)' if is_valid else 'Invalid Card Number.'
        dialog = ResultDialog(message, is_valid)
        dialog.exec()

    def show_how(self):
        how_dialog = HowDialog()
        how_dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CardValidatorApp()
    window.show()
    sys.exit(app.exec())
