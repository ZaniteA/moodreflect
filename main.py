import sys
from PyQt6.QtWidgets import QApplication

from main_app import MoodReflectApp



def main():
    app = QApplication(sys.argv)
    window = MoodReflectApp()
    window.show()

    sys.exit(app.exec())



if __name__ == '__main__':
    main()
