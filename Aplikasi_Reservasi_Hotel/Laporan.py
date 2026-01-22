import sys
import os
from PyQt5 import QtWidgets, uic


class Laporan(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load UI laporan
        ui_path = os.path.join(os.path.dirname(__file__), "Laporan.ui")
        uic.loadUi(ui_path, self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Laporan()
    window.show()
    sys.exit(app.exec_())
