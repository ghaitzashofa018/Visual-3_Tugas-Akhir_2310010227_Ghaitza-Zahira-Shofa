import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from koneksi import get_connection


class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # LOAD UI DULU (WAJIB)
        ui_path = os.path.join(os.path.dirname(__file__), "Login.ui")
        uic.loadUi(ui_path, self)

        # tombol login (tanpa objectName)
        buttons = self.findChildren(QtWidgets.QPushButton)
        if buttons:
            buttons[0].clicked.connect(self.proses_login)

    def proses_login(self):
        inputs = self.findChildren(QtWidgets.QLineEdit)
        username = inputs[0].text()
        password = inputs[1].text()

        if username == "admin" and password == "pass123":
            QMessageBox.information(self, "Login", "Login berhasil")

            # IMPORT DASHBOARD DI SINI (ANTI ERROR)
            from dashboard import Dashboard
            self.dashboard = Dashboard()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login", "Username atau Password salah")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
