import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox


class Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "dashboard.ui")
        uic.loadUi(ui_path, self)

        # =============================
        # HUBUNGKAN SEMUA TOMBOL MENU
        # =============================
        self.kamarBtn.clicked.connect(self.open_kamar)
        self.laporanBtn.clicked.connect(self.open_laporan)
        self.reservasiBtn.clicked.connect(self.open_reservasi)
        self.pelangganBtn.clicked.connect(self.open_pelanggan)
        self.pembayaranBtn.clicked.connect(self.open_pembayaran)
        self.logoutBtn.clicked.connect(self.logout)

    # =============================
    # FUNGSI NAVIGASI
    # =============================
    def open_kamar(self):
        from kamar import Kamar
        self.kamar = Kamar()
        self.kamar.show()

    def open_laporan(self):
        from Laporan import Laporan  # pastikan nama file BENAR
        self.laporan = Laporan()
        self.laporan.show()

    def open_reservasi(self):
        from reservasi import ReservasiWindow
        self.reservasi = ReservasiWindow()
        self.reservasi.show()

    def open_pelanggan(self):
        from pelanggan import PelangganWindow
        self.pelanggan = PelangganWindow()
        self.pelanggan.show()

    def open_pembayaran(self):
        from pembayaran import PembayaranWindow
        self.pembayaran = PembayaranWindow()
        self.pembayaran.show()

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Logout",
            "Yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            from Login import Login
            self.login = Login()
            self.login.show()
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
