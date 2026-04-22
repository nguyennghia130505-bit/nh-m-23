"""
views/meter_view.py - Màn hình Quản lý Công tơ Điện
Hiển thị danh sách công tơ, trạng thái và thông tin liên kết khách hàng
"""

import copy
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QHeaderView, QAbstractItemView,
    QFrame, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data.mock_data import METERS


class MeterView(QWidget):
    """
    Màn hình Quản lý Công tơ Điện.
    Hiển thị mã công tơ, khách hàng liên kết, vị trí và trạng thái.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.meters = copy.deepcopy(METERS)
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        """Xây dựng giao diện"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("⚡ Quản lý Công tơ Điện")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(header)

        # ── Toolbar ──────────────────────────────────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Tìm kiếm
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍  Tìm kiếm theo mã công tơ, khách hàng...")
        self.txt_search.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 16px;
                background: #FFFFFF;
                min-height: 36px;
            }
            QLineEdit:focus { border-color: #3B82F6; }
        """)
        self.txt_search.textChanged.connect(self._on_search)
        toolbar.addWidget(self.txt_search, stretch=1)

        # Lọc theo trạng thái
        self.cmb_filter = QComboBox()
        self.cmb_filter.addItems(["Tất cả", "Hoạt động", "Hỏng", "Ngừng"])
        self.cmb_filter.setStyleSheet("""
            QComboBox {
                border: 1.5px solid #E2E8F0;
                border-radius: 8px;
                padding: 7px 14px;
                font-size: 16px;
                background: #FFFFFF;
                min-height: 36px;
                min-width: 130px;
            }
            QComboBox:focus { border-color: #3B82F6; }
        """)
        self.cmb_filter.currentTextChanged.connect(self._on_filter_changed)
        toolbar.addWidget(self.cmb_filter)

        # Nút làm mới
        btn_style = """
            QPushButton {{
                background: {bg}; color: {fg};
                border: none; border-radius: 7px;
                padding: 8px 18px; font-size: 16px;
                font-weight: 600; min-height: 36px;
            }}
            QPushButton:hover {{ background: {hover}; }}
        """
        self.btn_refresh = QPushButton("🔄  Làm mới")
        self.btn_refresh.setStyleSheet(btn_style.format(bg="#6B7280", fg="white", hover="#4B5563"))
        self.btn_refresh.clicked.connect(self._on_refresh)
        toolbar.addWidget(self.btn_refresh)

        main_layout.addLayout(toolbar)

        # ── Thẻ tóm tắt trạng thái ──────────────────────────
        summary = QHBoxLayout()
        summary.setSpacing(12)
        total = len(self.meters)
        active = sum(1 for m in self.meters if m["trang_thai"] == "Hoạt động")
        broken = sum(1 for m in self.meters if m["trang_thai"] == "Hỏng")

        for label, value, color in [
            ("Tổng số", total, "#3B82F6"),
            ("Hoạt động", active, "#10B981"),
            ("Đang hỏng", broken, "#EF4444"),
        ]:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: #FFFFFF;
                    border-radius: 8px;
                    border-left: 4px solid {color};
                }}
            """)
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 10, 16, 10)
            lbl = QLabel(f"<b style='font-size:22px; color:{color}'>{value}</b>  "
                         f"<span style='font-size:12px; color:#64748B'>{label}</span>")
            lbl.setTextFormat(Qt.RichText)
            card_layout.addWidget(lbl)
            summary.addWidget(card)

        main_layout.addLayout(summary)

        # ── Bảng dữ liệu ────────────────────────────────────
        self.table = QTableWidget()
        columns = ["Mã Công tơ", "Mã KH", "Tên Khách hàng", "Vị trí lắp đặt", "Trạng thái"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 110)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 80)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 120)

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
            QTableWidget::item {
                padding: 10px 12px;
                border-bottom: 1px solid #F1F5F9;
            }
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

        # Thanh đếm
        self.lbl_count = QLabel("Tổng: 0 công tơ")
        self.lbl_count.setStyleSheet("font-size: 16px; color: #64748B;")
        main_layout.addWidget(self.lbl_count)

    def _load_table(self, data: list = None):
        """Nạp dữ liệu vào bảng"""
        if data is None:
            data = self.meters

        self.table.setRowCount(0)
        color_map = {"Hoạt động": "#10B981", "Hỏng": "#EF4444", "Ngừng": "#F59E0B"}

        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, key in enumerate(["ma_cong_to", "ma_kh", "ten_kh", "vi_tri", "trang_thai"]):
                text = row_data.get(key, "")
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if key == "trang_thai":
                    item.setForeground(QColor(color_map.get(text, "#64748B")))
                self.table.setItem(row_idx, col_idx, item)

        self.lbl_count.setText(f"Tổng: {len(data)} công tơ")

    def _on_search(self, keyword: str):
        """Lọc theo từ khóa"""
        keyword = keyword.lower().strip()
        filter_val = self.cmb_filter.currentText()
        filtered = self._apply_filter(self.meters, filter_val)
        if keyword:
            filtered = [
                m for m in filtered
                if keyword in m["ma_cong_to"].lower()
                or keyword in m["ten_kh"].lower()
                or keyword in m["ma_kh"].lower()
            ]
        self._load_table(filtered)

    def _on_filter_changed(self, value: str):
        """Lọc theo trạng thái"""
        keyword = self.txt_search.text().lower().strip()
        filtered = self._apply_filter(self.meters, value)
        if keyword:
            filtered = [
                m for m in filtered
                if keyword in m["ma_cong_to"].lower() or keyword in m["ten_kh"].lower()
            ]
        self._load_table(filtered)

    def _apply_filter(self, data: list, filter_val: str) -> list:
        """Áp dụng bộ lọc trạng thái"""
        if filter_val == "Tất cả":
            return data
        return [m for m in data if m["trang_thai"] == filter_val]

    def _on_refresh(self):
        """Làm mới"""
        self.txt_search.clear()
        self.cmb_filter.setCurrentIndex(0)
        self._load_table()
