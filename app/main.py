import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)

    font = QFont("Segoe UI")
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()