"""
views/invoice_view.py - Màn hình Hóa đơn
Danh sách hóa đơn, in hóa đơn ra console
"""

import copy
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QHeaderView, QAbstractItemView,
    QMessageBox, QFrame, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data.db_repository import get_all_invoices, update_invoice_status


class InvoiceView(QWidget):
    """
    Màn hình Hóa đơn.
    Hiển thị danh sách hóa đơn, cho phép xem chi tiết và in ra console.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.invoices = []
        self._build_ui()
        self._refresh_data()

    def _refresh_data(self):
        self.invoices = get_all_invoices()
        self._load_table()

    def _build_ui(self):
        """Xây dựng giao diện"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("🧾 Quản lý Hóa đơn")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(header)

        # ── Tóm tắt ─────────────────────────────────────────
        summary_h = QHBoxLayout()
        summary_h.setSpacing(12)

        tong = len(self.invoices)
        da_tt = sum(1 for i in self.invoices if i["trang_thai"] == "Đã thanh toán")
        chua_tt = sum(1 for i in self.invoices if i["trang_thai"] == "Chưa thanh toán")
        tong_tt = sum(i["tong_tien"] for i in self.invoices if i["trang_thai"] == "Đã thanh toán")

        for label, value, color in [
            ("Tổng hóa đơn", str(tong), "#3B82F6"),
            ("Đã thanh toán", str(da_tt), "#10B981"),
            ("Chưa thanh toán", str(chua_tt), "#EF4444"),
            ("Doanh thu", f"{tong_tt:,.0f}đ", "#F59E0B"),
        ]:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: #FFFFFF;
                    border-radius: 8px;
                    border-left: 4px solid {color};
                }}
            """)
            card_h = QHBoxLayout(card)
            card_h.setContentsMargins(14, 10, 14, 10)
            lbl = QLabel(
                f"<b style='font-size:20px; color:{color}'>{value}</b><br/>"
                f"<span style='font-size:11px; color:#64748B'>{label}</span>"
            )
            lbl.setTextFormat(Qt.RichText)
            card_h.addWidget(lbl)
            summary_h.addWidget(card)

        main_layout.addLayout(summary_h)

        # ── Toolbar ──────────────────────────────────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍  Tìm kiếm theo mã HĐ, khách hàng...")
        self.txt_search.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #E2E8F0; border-radius: 8px;
                padding: 8px 14px; font-size: 16px;
                background: #FFFFFF; min-height: 36px;
            }
            QLineEdit:focus { border-color: #3B82F6; }
        """)
        self.txt_search.textChanged.connect(self._on_search)
        toolbar.addWidget(self.txt_search, stretch=1)

        self.cmb_filter = QComboBox()
        self.cmb_filter.addItems(["Tất cả", "Đã thanh toán", "Chưa thanh toán"])
        self.cmb_filter.setStyleSheet("""
            QComboBox {
                border: 1.5px solid #E2E8F0; border-radius: 8px;
                padding: 7px 14px; font-size: 16px;
                background: #FFFFFF; min-height: 36px; min-width: 160px;
            }
            QComboBox:focus { border-color: #3B82F6; }
        """)
        self.cmb_filter.currentTextChanged.connect(self._on_filter_changed)
        toolbar.addWidget(self.cmb_filter)

        btn_style = """
            QPushButton {{
                background: {bg}; color: {fg};
                border: none; border-radius: 7px;
                padding: 8px 18px; font-size: 16px;
                font-weight: 600; min-height: 36px;
            }}
            QPushButton:hover {{ background: {hover}; }}
        """
        self.btn_print = QPushButton("🖨️  In hóa đơn")
        self.btn_print.setStyleSheet(btn_style.format(bg="#3B82F6", fg="white", hover="#2563EB"))

        self.btn_mark_paid = QPushButton("✅  Đánh dấu đã TT")
        self.btn_mark_paid.setStyleSheet(btn_style.format(bg="#10B981", fg="white", hover="#059669"))

        toolbar.addWidget(self.btn_print)
        toolbar.addWidget(self.btn_mark_paid)

        main_layout.addLayout(toolbar)

        # ── Bảng hóa đơn ────────────────────────────────────
        self.table = QTableWidget()
        columns = ["Mã HĐ", "Mã CT", "Mã KH", "Tên Khách hàng", "Tháng", "Tiêu thụ", "Tổng tiền", "Trạng thái"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 80)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 80)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 80)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 80)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 100)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)
        self.table.setColumnWidth(7, 130)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #FFFFFF; border-radius: 10px;
                border: none; font-size: 16px; color: #1E293B;
            }
            QTableWidget::item { padding: 10px 12px; border-bottom: 1px solid #F1F5F9; }
            QTableWidget::item:selected { background: #EFF6FF; color: #1D4ED8; }
            QHeaderView::section {
                background: #F8FAFC; color: #64748B;
                font-size: 16px; font-weight: bold;
                padding: 10px 12px; border: none;
                border-bottom: 2px solid #E2E8F0;
            }
            QTableWidget::item:alternate { background: #F8FAFC; }
        """)
        main_layout.addWidget(self.table)

        self.lbl_count = QLabel("Tổng: 0 hóa đơn")
        self.lbl_count.setStyleSheet("font-size: 16px; color: #64748B;")
        main_layout.addWidget(self.lbl_count)

        # Kết nối signal-slot
        self.btn_print.clicked.connect(self._on_print)
        self.btn_mark_paid.clicked.connect(self._on_mark_paid)
        self.table.doubleClicked.connect(self._on_print)

    def _load_table(self, data: list = None):
        """Nạp dữ liệu vào bảng"""
        if data is None:
            data = self.invoices

        self.table.setRowCount(0)
        color_map = {"Đã thanh toán": "#10B981", "Chưa thanh toán": "#EF4444"}

        for row_idx, inv in enumerate(data):
            self.table.insertRow(row_idx)
            row_vals = [
                inv["ma_hd"], inv.get("ma_cong_to", ""), inv["ma_kh"], inv["ten_kh"],
                inv["thang"], f"{inv['tieu_thu']} kWh",
                f"{inv['tong_tien']:,.0f}đ", inv["trang_thai"]
            ]
            for col_idx, text in enumerate(row_vals):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col_idx == 6:
                    item.setForeground(QColor("#1D4ED8"))
                if col_idx == 7:
                    item.setForeground(QColor(color_map.get(text, "#64748B")))
                self.table.setItem(row_idx, col_idx, item)

        self.lbl_count.setText(f"Tổng: {len(data)} hóa đơn")

    def _get_selected_invoice(self):
        """Trả về hóa đơn đang được chọn"""
        row = self.table.currentRow()
        if row < 0:
            return None
        ma_hd = self.table.item(row, 0).text()
        return next((i for i in self.invoices if i["ma_hd"] == ma_hd), None)

    def _on_print(self):
        """In hóa đơn ra console"""
        inv = self._get_selected_invoice()
        if inv is None:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn hóa đơn cần in!")
            return

        # In ra console
        separator = "=" * 50
        print(f"\n{separator}")
        print(f"        HÓA ĐƠN TIỀN ĐIỆN")
        print(f"    Điện lực Khu Dân Cư - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(separator)
        print(f"  Mã hóa đơn  : {inv['ma_hd']}")
        print(f"  Khách hàng  : {inv['ten_kh']} ({inv['ma_kh']})")
        print(f"  Kỳ tháng    : {inv['thang']}")
        print(f"  Điện tiêu thụ: {inv['tieu_thu']} kWh")
        print(f"  Tổng tiền   : {inv['tong_tien']:,.0f} VNĐ")
        print(f"  Trạng thái  : {inv['trang_thai']}")
        print(separator)
        print(f"  Cảm ơn quý khách đã sử dụng dịch vụ!")
        print(f"{separator}\n")

        QMessageBox.information(
            self, "In hóa đơn",
            f"✅ Đã in hóa đơn {inv['ma_hd']}!\n\nXem chi tiết trong cửa sổ console/terminal."
        )

    def _on_mark_paid(self):
        """Đánh dấu đã thanh toán"""
        inv = self._get_selected_invoice()
        if inv is None:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn hóa đơn!")
            return
        if inv["trang_thai"] == "Đã thanh toán":
            QMessageBox.information(self, "Thông báo", "Hóa đơn này đã được thanh toán!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận",
            f"Xác nhận thanh toán hóa đơn {inv['ma_hd']} - {inv['ten_kh']}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = update_invoice_status(inv["ma_hd"], "Đã thanh toán", datetime.now().strftime('%d/%m/%Y'))
            if success:
                self._refresh_data()
                print(f"[INVOICE] Đã thanh toán: {inv['ma_hd']}")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể cập nhật CSDL!")

    def _on_search(self, keyword: str):
        """Tìm kiếm hóa đơn"""
        keyword = keyword.lower()
        filter_val = self.cmb_filter.currentText()
        filtered = self._apply_filter(self.invoices, filter_val)
        if keyword:
            filtered = [
                i for i in filtered
                if keyword in i["ma_hd"].lower() or keyword in i["ten_kh"].lower()
            ]
        self._load_table(filtered)

    def _on_filter_changed(self, value: str):
        """Lọc theo trạng thái thanh toán"""
        keyword = self.txt_search.text().lower()
        filtered = self._apply_filter(self.invoices, value)
        if keyword:
            filtered = [
                i for i in filtered
                if keyword in i["ma_hd"].lower() or keyword in i["ten_kh"].lower()
            ]
        self._load_table(filtered)

    def _apply_filter(self, data, filter_val):
        if filter_val == "Tất cả":
            return data
        return [i for i in data if i["trang_thai"] == filter_val]
