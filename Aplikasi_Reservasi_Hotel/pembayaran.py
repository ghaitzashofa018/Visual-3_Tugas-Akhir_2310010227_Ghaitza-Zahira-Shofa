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

# ================= WINDOW PEMBAYARAN =================
class PembayaranWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load UI
        ui_path = os.path.join(os.path.dirname(__file__), "pembayaran.ui")
        uic.loadUi(ui_path, self)

        self.selected_id = None

        # event
        self.statusFilter.currentIndexChanged.connect(self.load_data)
        self.metodeFilter.currentIndexChanged.connect(self.load_data)
        self.pembayaranTable.cellClicked.connect(self.pilih_data)
        self.verifiBtn.clicked.connect(self.verifikasi_pembayaran)
        self.printBtn.clicked.connect(self.print_data)

        # load data awal
        self.load_data()

    # ================= LOAD DATA =================
    def load_data(self):
        try:
            status = self.statusFilter.currentText()
            metode = self.metodeFilter.currentText()

            conn = koneksi()
            cursor = conn.cursor()

            sql = """
                SELECT 
                    id_pembayaran,
                    id_reservasi,
                    jumlah_bayar,
                    metode_bayar,
                    tanggal_bayar,
                    status_pembayaran,
                    bukti_bayar
                FROM pembayaran
                WHERE 1=1
            """
            params = []

            if status != "Semua Status":
                sql += " AND status_pembayaran=%s"
                params.append(status)

            if metode != "Semua Metode":
                sql += " AND metode_bayar=%s"
                params.append(metode)

            cursor.execute(sql, params)
            data = cursor.fetchall()
            conn.close()

            self.pembayaranTable.setRowCount(0)

            for row_data in data:
                row = self.pembayaranTable.rowCount()
                self.pembayaranTable.insertRow(row)

                for col, value in enumerate(row_data):
                    self.pembayaranTable.setItem(
                        row, col, QTableWidgetItem(str(value))
                    )

                # kolom aksi
                self.pembayaranTable.setItem(
                    row, 7, QTableWidgetItem("Lihat")
                )

            self.totalLabel.setText(f"Total Pembayaran: {len(data)}")

        except Exception as e:
            QMessageBox.warning(self, "Error Load Data", str(e))

    # ================= PILIH DATA =================
    def pilih_data(self, row, column):
        item = self.pembayaranTable.item(row, 0)
        if item:
            self.selected_id = item.text()

    # ================= VERIFIKASI =================
    def verifikasi_pembayaran(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        try:
            conn = koneksi()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE pembayaran
                SET status_pembayaran='Berhasil'
                WHERE id_pembayaran=%s
            """, (self.selected_id,))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Sukses", "Pembayaran berhasil diverifikasi")
            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Error Verifikasi", str(e))

    # ================= PRINT =================
    def print_data(self):
        QMessageBox.information(
            self,
            "Print",
            "Fitur print belum diaktifkan"
        )

    # ================= KEMBALI DASHBOARD (OPSIONAL) =================
    def kembali_dashboard(self):
        from dashboard import Dashboard
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()

# ================= MAIN =================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PembayaranWindow()
    window.show()
    sys.exit(app.exec_())
