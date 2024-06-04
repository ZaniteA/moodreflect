import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from main_app import MoodReflectApp
import utilities

try:
    from ctypes import windll  # Only exists on Windows
    myappid = 'com.moodreflect.v1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass



def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(utilities.adjust_path('assets/logo/moodreflect_icon.png')))
    window = MoodReflectApp()
    window.show()

    sys.exit(app.exec())



if __name__ == '__main__':
    main()
