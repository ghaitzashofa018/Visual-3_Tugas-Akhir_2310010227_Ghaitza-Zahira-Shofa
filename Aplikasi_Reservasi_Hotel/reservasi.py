import sys
import os
import pymysql
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

# ================= KONEKSI DATABASE =================
def koneksi():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="db_reservasi_hotel"
    )

# ================= WINDOW RESERVASI =================
class ReservasiWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load UI
        ui_path = os.path.join(os.path.dirname(__file__), "reservasi.ui")
        uic.loadUi(ui_path, self)

        # event tombol (sesuai UI)
        self.refreshBtn.clicked.connect(self.load_data)
        self.tambahBtn.clicked.connect(self.tambah_data)
        self.searchInput.textChanged.connect(self.cari_data)
        self.filterStatus.currentTextChanged.connect(self.filter_data)

        # load data awal
        self.load_data()

    # ================= LOAD DATA =================
    def load_data(self):
        try:
            conn = koneksi()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservasi")
            data = cursor.fetchall()
            conn.close()

            self.reservasiTable.setRowCount(0)

            for row_data in data:
                row = self.reservasiTable.rowCount()
                self.reservasiTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.reservasiTable.setItem(
                        row, col, QTableWidgetItem(str(value))
                    )

            self.totalLabel.setText(f"Total: {len(data)} Reservasi")

        except Exception as e:
            QMessageBox.warning(self, "Error Load Data", str(e))

    # ================= TAMBAH DATA =================
    def tambah_data(self):
        QMessageBox.information(
            self,
            "Info",
            "Fitur tambah reservasi belum diimplementasikan"
        )

    # ================= CARI DATA =================
    def cari_data(self):
        keyword = self.searchInput.text()

        try:
            conn = koneksi()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reservasi
                WHERE id_reservasi LIKE %s
                   OR status_reservasi LIKE %s
            """, (f"%{keyword}%", f"%{keyword}%"))

            data = cursor.fetchall()
            conn.close()

            self.reservasiTable.setRowCount(0)

            for row_data in data:
                row = self.reservasiTable.rowCount()
                self.reservasiTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.reservasiTable.setItem(
                        row, col, QTableWidgetItem(str(value))
                    )

        except Exception as e:
            QMessageBox.warning(self, "Error Cari Data", str(e))

    # ================= FILTER STATUS =================
    def filter_data(self):
        status = self.filterStatus.currentText()

        try:
            conn = koneksi()
            cursor = conn.cursor()

            if status == "Semua Status":
                cursor.execute("SELECT * FROM reservasi")
            else:
                cursor.execute(
                    "SELECT * FROM reservasi WHERE status_reservasi=%s",
                    (status,)
                )

            data = cursor.fetchall()
            conn.close()

            self.reservasiTable.setRowCount(0)

            for row_data in data:
                row = self.reservasiTable.rowCount()
                self.reservasiTable.insertRow(row)
                for col, value in enumerate(row_data):
                    self.reservasiTable.setItem(
                        row, col, QTableWidgetItem(str(value))
                    )

        except Exception as e:
            QMessageBox.warning(self, "Error Filter Data", str(e))

    # ================= KEMBALI DASHBOARD (OPSIONAL) =================
    def kembali_dashboard(self):
        from dashboard import Dashboard
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()


# ================= MAIN =================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ReservasiWindow()
    window.show()
    sys.exit(app.exec_())
