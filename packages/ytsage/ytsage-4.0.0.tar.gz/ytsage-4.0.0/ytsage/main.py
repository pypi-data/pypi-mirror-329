import sys
from PySide6.QtWidgets import QApplication
from .ytsage_gui import YTSageApp

def main():
    app = QApplication(sys.argv)
    window = YTSageApp() # Instantiate the main application class
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()