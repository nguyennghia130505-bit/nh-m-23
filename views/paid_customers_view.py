"""
views/paid_customers_view.py - Màn hình Danh sách Khách hàng Đã Thanh Toán
Lọc theo tháng, hiển thị chi tiết, thống kê tổng doanh thu đã thu
"""

import copy
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QHeaderView, QAbstractItemView,
    QFrame, QComboBox, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont

from data.db_repository import get_invoices_history


# ── Bảng màu ────────────────────────────────────────────────
CLR_GREEN     = "#10B981"
CLR_BLUE      = "#3B82F6"
CLR_AMBER     = "#F59E0B"
CLR_SLATE_BG  = "#F1F5F9"
CLR_WHITE     = "#FFFFFF"
CLR_DARK      = "#1E293B"
CLR_MUTED     = "#64748B"
CLR_BORDER    = "#E2E8F0"
GRAD_SIDEBAR  = "qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1E3A5F,stop:1 #0F2744)"


class PaidCustomersView(QWidget):
    """
    Màn hình Danh sách Khách hàng Đã Thanh Toán Theo Tháng.

    Tính năng:
      - Lọc theo tháng (combobox với tất cả tháng có dữ liệu)
      - Tìm kiếm nhanh theo mã KH / tên KH
      - Bảng danh sách chi tiết (mã HĐ, khách hàng, địa chỉ, kWh, tiền, ngày TT)
      - Thẻ thống kê: tổng KH đã TT, tổng kWh, tổng doanh thu
      - Nút xuất / in danh sách ra console
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_data = []
        self._build_ui()
        self._load_data_and_refresh()

    def _load_data_and_refresh(self):
        self._all_data = get_invoices_history()
        self._populate_month_combo()
        self._refresh()

    # ── Xây dựng giao diện ─────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # ── Tiêu đề ──────────────────────────────────────────
        hdr_row = QHBoxLayout()
        lbl_title = QLabel("✅  Khách Hàng Đã Thanh Toán Theo Tháng")
        lbl_title.setStyleSheet(
            "font-size: 26px; font-weight: bold; color: #1E293B;"
        )
        hdr_row.addWidget(lbl_title)
        hdr_row.addStretch()
        root.addLayout(hdr_row)

        # ── Thẻ thống kê ─────────────────────────────────────
        self._stat_row = QHBoxLayout()
        self._stat_row.setSpacing(14)

        self._card_count   = self._make_stat_card("Khách đã thanh toán", "0",    CLR_GREEN)
        self._card_kwh     = self._make_stat_card("Tổng điện tiêu thụ",  "0 kWh", CLR_BLUE)
        self._card_revenue = self._make_stat_card("Doanh thu thu được",  "0 đ",   CLR_AMBER)

        for card in (self._card_count, self._card_kwh, self._card_revenue):
            self._stat_row.addWidget(card["frame"])

        root.addLayout(self._stat_row)

        # ── Thanh công cụ ─────────────────────────────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Combo lọc tháng
        lbl_month = QLabel("📅 Tháng:")
        lbl_month.setStyleSheet("font-size: 16px; font-weight: 600; color: #374151;")
        toolbar.addWidget(lbl_month)

        self.cmb_month = QComboBox()
        self.cmb_month.setFixedWidth(160)
        self.cmb_month.setStyleSheet(self._combo_style())
        self.cmb_month.currentTextChanged.connect(self._refresh)
        toolbar.addWidget(self.cmb_month)

        toolbar.addSpacing(14)

        # Tìm kiếm
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍  Tìm theo mã KH, tên khách hàng...")
        self.txt_search.setStyleSheet(self._input_style())
        self.txt_search.textChanged.connect(self._refresh)
        toolbar.addWidget(self.txt_search, stretch=1)

        # Nút in danh sách
        self.btn_print = QPushButton("🖨️  In danh sách")
        self.btn_print.setStyleSheet(
            self._btn_style(CLR_BLUE, "#2563EB")
        )
        self.btn_print.clicked.connect(self._on_print)
        toolbar.addWidget(self.btn_print)

        # Nút làm mới
        self.btn_refresh = QPushButton("🔄  Làm mới")
        self.btn_refresh.setStyleSheet(
            self._btn_style("#64748B", "#475569")
        )
        self.btn_refresh.clicked.connect(self._on_reset)
        toolbar.addWidget(self.btn_refresh)

        root.addLayout(toolbar)

        # ── Bảng dữ liệu ────────────────────────────────────
        cols = [
            "Mã HĐ", "Mã CT", "Mã KH", "Tên Khách hàng",
            "Địa chỉ", "Tháng", "Tiêu thụ",
            "Tổng tiền", "Ngày thanh toán"
        ]
        self.table = QTableWidget()
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)
        # Cột cố định
        for col_idx, width in [(0, 100), (1, 80), (2, 80), (4, 240), (5, 90), (6, 100), (8, 130)]:
            hh.setSectionResizeMode(col_idx, QHeaderView.Fixed)
            self.table.setColumnWidth(col_idx, width)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(self._table_style())
        self.table.setSortingEnabled(True)
        root.addWidget(self.table)

        # ── Trạng thái dưới bảng ─────────────────────────────
        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet("font-size: 15px; color: #64748B;")
        root.addWidget(self.lbl_status)

    # ── Tạo thẻ thống kê ────────────────────────────────────
    def _make_stat_card(self, label: str, value: str, color: str) -> dict:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {CLR_WHITE};
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
        """)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frame.setMinimumHeight(78)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(4)

        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(
            f"font-size: 24px; font-weight: bold; color: {color};"
        )
        lbl_name = QLabel(label)
        lbl_name.setStyleSheet("font-size: 13px; color: #64748B;")

        layout.addWidget(lbl_val)
        layout.addWidget(lbl_name)

        return {"frame": frame, "value_label": lbl_val, "name_label": lbl_name}

    def _update_stat_card(self, card: dict, value: str):
        card["value_label"].setText(value)

    # ── Populate combo tháng ─────────────────────────────────
    def _populate_month_combo(self):
        self.cmb_month.blockSignals(True)
        months = sorted(
            {inv["thang"] for inv in self._all_data},
            key=lambda m: (int(m.split("/")[1]), int(m.split("/")[0])),
            reverse=True,
        )
        self.cmb_month.addItem("Tất cả tháng")
        for m in months:
            self.cmb_month.addItem(m)
        self.cmb_month.blockSignals(False)

    # ── Lấy dữ liệu đã lọc ──────────────────────────────────
    def _get_filtered_data(self) -> list:
        month     = self.cmb_month.currentText()
        keyword   = self.txt_search.text().strip().lower()

        result = [inv for inv in self._all_data if inv["trang_thai"] == "Đã thanh toán"]

        if month and month != "Tất cả tháng":
            result = [inv for inv in result if inv["thang"] == month]

        if keyword:
            result = [
                inv for inv in result
                if keyword in inv["ma_kh"].lower()
                or keyword in inv["ten_kh"].lower()
                or keyword in inv.get("ma_hd", "").lower()
            ]

        return result

    # ── Làm mới bảng & thống kê ─────────────────────────────
    def _refresh(self):
        data = self._get_filtered_data()
        self._load_table(data)
        self._update_stats(data)

    def _load_table(self, data: list):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for row_idx, inv in enumerate(data):
            self.table.insertRow(row_idx)
            row_vals = [
                inv.get("ma_hd", ""),
                inv.get("ma_cong_to", ""),
                inv.get("ma_kh", ""),
                inv.get("ten_kh", ""),
                inv.get("dia_chi", ""),
                inv.get("thang", ""),
                f"{inv.get('tieu_thu', 0)} kWh",
                f"{inv.get('tong_tien', 0):,.0f} đ",
                inv.get("ngay_tt", ""),
            ]
            alignments = [
                Qt.AlignCenter, Qt.AlignCenter, Qt.AlignCenter, Qt.AlignVCenter | Qt.AlignLeft,
                Qt.AlignVCenter | Qt.AlignLeft, Qt.AlignCenter,
                Qt.AlignCenter, Qt.AlignCenter, Qt.AlignCenter,
            ]
            for col_idx, (text, align) in enumerate(zip(row_vals, alignments)):
                item = QTableWidgetItem(text)
                item.setTextAlignment(align)
                if col_idx == 6:
                    item.setForeground(QColor(CLR_GREEN))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                if col_idx == 7:
                    item.setForeground(QColor(CLR_BLUE))
                self.table.setItem(row_idx, col_idx, item)

            self.table.setRowHeight(row_idx, 42)

        self.table.setSortingEnabled(True)
        self.lbl_status.setText(
            f"Hiển thị {len(data)} khách hàng đã thanh toán"
            + (f"  —  Tháng: {self.cmb_month.currentText()}"
               if self.cmb_month.currentText() != "Tất cả tháng" else "")
        )

    def _update_stats(self, data: list):
        total_kh      = len(data)
        total_kwh     = sum(inv.get("tieu_thu", 0) for inv in data)
        total_revenue = sum(inv.get("tong_tien", 0) for inv in data)

        self._update_stat_card(self._card_count,   str(total_kh))
        self._update_stat_card(self._card_kwh,     f"{total_kwh:,} kWh")
        self._update_stat_card(self._card_revenue, f"{total_revenue:,.0f} đ")

    # ── Nút hành động ────────────────────────────────────────
    def _on_print(self):
        data = self._get_filtered_data()
        if not data:
            QMessageBox.information(self, "Thông báo", "Không có dữ liệu để in!")
            return

        month_str = self.cmb_month.currentText()
        sep = "=" * 70
        print(f"\n{sep}")
        print(f"  DANH SÁCH KHÁCH HÀNG ĐÃ THANH TOÁN  —  {month_str.upper()}")
        print(sep)
        print(f"  {'STT':<5} {'Mã KH':<10} {'Tên khách hàng':<22} "
              f"{'Tháng':<10} {'kWh':>6} {'Tổng tiền':>15}  {'Ngày TT':<13}")
        print("-" * 70)
        tong = 0
        for i, inv in enumerate(data, 1):
            print(f"  {i:<5} {inv['ma_kh']:<10} {inv['ten_kh']:<22} "
                  f"{inv['thang']:<10} {inv['tieu_thu']:>6} "
                  f"{inv['tong_tien']:>14,.0f}đ  {inv.get('ngay_tt',''):<13}")
            tong += inv["tong_tien"]
        print("-" * 70)
        print(f"  {'TỔNG DOANH THU':>50}  {tong:>14,.0f}đ")
        print(f"{sep}\n")

        QMessageBox.information(
            self, "In danh sách",
            f"✅ Đã in danh sách {len(data)} khách hàng!\n\nXem chi tiết trong cửa sổ console/terminal."
        )

    def _on_reset(self):
        self._all_data = get_invoices_history()
        self._populate_month_combo()
        self.cmb_month.setCurrentIndex(0)
        self.txt_search.clear()
        self._refresh()

    # ── Stylesheet helpers ───────────────────────────────────
    @staticmethod
    def _combo_style() -> str:
        return """
            QComboBox {
                border: 1.5px solid #E2E8F0; border-radius: 8px;
                padding: 7px 12px; font-size: 16px;
                background: #FFFFFF; min-height: 36px;
            }
            QComboBox:focus { border-color: #3B82F6; }
            QComboBox::drop-down { border: none; width: 28px; }
        """

    @staticmethod
    def _input_style() -> str:
        return """
            QLineEdit {
                border: 1.5px solid #E2E8F0; border-radius: 8px;
                padding: 8px 14px; font-size: 16px;
                background: #FFFFFF; min-height: 36px;
            }
            QLineEdit:focus { border-color: #3B82F6; }
        """

    @staticmethod
    def _btn_style(bg: str, hover: str) -> str:
        return f"""
            QPushButton {{
                background: {bg}; color: white;
                border: none; border-radius: 8px;
                padding: 8px 18px; font-size: 16px;
                font-weight: 600; min-height: 36px;
            }}
            QPushButton:hover {{ background: {hover}; }}
        """

    @staticmethod
    def _table_style() -> str:
        return """
            QTableWidget {
                background: #FFFFFF; border-radius: 10px;
                border: none; font-size: 15px; color: #1E293B;
            }
            QTableWidget::item {
                padding: 8px 10px;
                border-bottom: 1px solid #F1F5F9;
            }
            QTableWidget::item:selected {
                background: #ECFDF5; color: #065F46;
            }
            QHeaderView::section {
                background: #F0FDF4; color: #065F46;
                font-size: 15px; font-weight: bold;
                padding: 10px 10px; border: none;
                border-bottom: 2px solid #6EE7B7;
            }
            QTableWidget::item:alternate { background: #F8FAFC; }
        """
