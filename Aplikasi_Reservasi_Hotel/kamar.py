import sys
import os
from PyQt5 import QtWidgets, uic

print("Start kamar.py")

class Kamar(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print("Init Kamar")

        ui_path = os.path.join(os.path.dirname(__file__), "kamar.ui")
        print("UI Path:", ui_path)

        uic.loadUi(ui_path, self)
        print("UI loaded")

        # tombol kembali (jangan import apa-apa dulu)
        if hasattr(self, "btnKembali"):
            self.btnKembali.clicked.connect(self.close)

        print("Setup selesai")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Kamar()
    window.show()
    print("Window shown")
    sys.exit(app.exec_())
