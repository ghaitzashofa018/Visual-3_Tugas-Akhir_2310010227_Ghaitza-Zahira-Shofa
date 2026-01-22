import sys
import os
import pymysql
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

# ===================== KONEKSI DATABASE =====================
def koneksi():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="db_reservasi_hotel"
    )

# ===================== WINDOW PELANGGAN =====================
class PelangganWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load UI
        ui_path = os.path.join(os.path.dirname(__file__), "pelanggan.ui")
        uic.loadUi(ui_path, self)

        # tombol kembali ke dashboard (WAJIB ADA di UI)
        if hasattr(self, "btnKembali"):
            self.btnKembali.clicked.connect(self.kembali_dashboard)

        # event
        self.searchInput.textChanged.connect(self.cari_data)
        self.tambahBtn.clicked.connect(self.notifikasi)

        # load data awal
        self.load_data()

    # ===================== LOAD DATA =====================
    def load_data(self):
        try:
            conn = koneksi()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    id_pelanggan,
                    nama_pelanggan,
                    email,
                    no_hp,
                    alamat,
                    tanggal_daftar,
                    status_pelanggan
                FROM pelanggan
            """)

            data = cursor.fetchall()
            conn.close()

            self.pelangganTable.setRowCount(0)
            self.pelangganTable.setColumnCount(8)
            self.pelangganTable.setHorizontalHeaderLabels([
                "ID", "Nama", "Email", "No HP",
                "Alamat", "Tgl Daftar", "Status", "Aksi"
            ])

            for row_data in data:
                row = self.pelangganTable.rowCount()
                self.pelangganTable.insertRow(row)

                for col, value in enumerate(row_data):
                    self.pelangganTable.setItem(
                        row, col, QTableWidgetItem(str(value))
                    )

                self.pelangganTable.setItem(
                    row, 7, QTableWidgetItem("Edit")
                )

            self.totalLabel.setText(f"Total: {len(data)} Pelanggan")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # ===================== CARI DATA =====================
    def cari_data(self):
        keyword = self.searchInput.text()

        conn = koneksi()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id_pelanggan,
                nama_pelanggan,
                email,
                no_hp,
                alamat,
                tanggal_daftar,
                status_pelanggan
            FROM pelanggan
            WHERE nama_pelanggan LIKE %s OR email LIKE %s
        """, (f"%{keyword}%", f"%{keyword}%"))

        data = cursor.fetchall()
        conn.close()

        self.pelangganTable.setRowCount(0)

        for row_data in data:
            row = self.pelangganTable.rowCount()
            self.pelangganTable.insertRow(row)

            for col, value in enumerate(row_data):
                self.pelangganTable.setItem(
                    row, col, QTableWidgetItem(str(value))
                )

            self.pelangganTable.setItem(
                row, 7, QTableWidgetItem("Edit")
            )

    # ===================== NOTIFIKASI =====================
    def notifikasi(self):
        QMessageBox.information(
            self,
            "Info",
            "Form tambah pelanggan belum tersedia"
        )

    # ===================== KEMBALI DASHBOARD =====================
    def kembali_dashboard(self):
        from dashboard import Dashboard
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()


# ===================== MAIN =====================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PelangganWindow()
    window.show()
    sys.exit(app.exec_())
