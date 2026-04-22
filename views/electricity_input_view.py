"""
views/electricity_input_view.py - Màn hình Nhập Chỉ số Điện
Chọn khách hàng, nhập chỉ số cũ/mới, tính điện tiêu thụ
"""

import copy
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data.mock_data import CUSTOMERS, ELECTRICITY_READINGS


class ElectricityInputView(QWidget):
    """
    Màn hình Nhập Chỉ số Điện.
    - Combobox chọn khách hàng
    - Input chỉ số cũ, chỉ số mới
    - Label hiển thị điện tiêu thụ = mới - cũ
    - Bảng lịch sử chỉ số đã nhập
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.readings = copy.deepcopy(ELECTRICITY_READINGS)
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        """Xây dựng giao diện"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("📝 Nhập Chỉ số Điện")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(header)

        # ── Form nhập chỉ số ────────────────────────────────
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame { background: #FFFFFF; border-radius: 12px; }
        """)
        form_outer = QVBoxLayout(form_frame)
        form_outer.setContentsMargins(24, 20, 24, 20)
        form_outer.setSpacing(16)

        form_title = QLabel("📋 Nhập thông tin chỉ số")
        form_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B;")
        form_outer.addWidget(form_title)

        grid = QGridLayout()
        grid.setSpacing(12)

        label_style = "font-size: 16px; font-weight: 600; color: #374151;"
        input_style = """
            QLineEdit, QComboBox {
                border: 1.5px solid #E2E8F0;
                border-radius: 7px;
                padding: 8px 12px;
                font-size: 17px;
                background: #F8FAFC;
                min-height: 40px;
            }
            QLineEdit:focus, QComboBox:focus { border-color: #3B82F6; background: #FFFFFF; }
        """

        # Row 0: Tháng, Khách hàng
        lbl_thang = QLabel("Tháng ghi chỉ số:")
        lbl_thang.setStyleSheet(label_style)
        self.txt_thang = QLineEdit("04/2026")
        self.txt_thang.setStyleSheet(input_style)

        lbl_kh = QLabel("Khách hàng:")
        lbl_kh.setStyleSheet(label_style)
        self.cmb_kh = QComboBox()
        self.cmb_kh.setStyleSheet(input_style)
        for c in CUSTOMERS:
            self.cmb_kh.addItem(f"{c['ma_kh']} - {c['ten']}", userData=c["ma_kh"])

        grid.addWidget(lbl_thang, 0, 0)
        grid.addWidget(self.txt_thang, 0, 1)
        grid.addWidget(lbl_kh, 0, 2)
        grid.addWidget(self.cmb_kh, 0, 3)

        # Row 1: Chỉ số cũ, Chỉ số mới
        lbl_cu = QLabel("Chỉ số cũ (kWh):")
        lbl_cu.setStyleSheet(label_style)
        self.txt_chi_so_cu = QLineEdit()
        self.txt_chi_so_cu.setPlaceholderText("Nhập chỉ số cũ...")
        self.txt_chi_so_cu.setStyleSheet(input_style)

        lbl_moi = QLabel("Chỉ số mới (kWh):")
        lbl_moi.setStyleSheet(label_style)
        self.txt_chi_so_moi = QLineEdit()
        self.txt_chi_so_moi.setPlaceholderText("Nhập chỉ số mới...")
        self.txt_chi_so_moi.setStyleSheet(input_style)

        grid.addWidget(lbl_cu, 1, 0)
        grid.addWidget(self.txt_chi_so_cu, 1, 1)
        grid.addWidget(lbl_moi, 1, 2)
        grid.addWidget(self.txt_chi_so_moi, 1, 3)

        form_outer.addLayout(grid)

        # ── Hiển thị điện tiêu thụ ──────────────────────────
        result_frame = QFrame()
        result_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #EFF6FF, stop:1 #F0FDF4);
                border-radius: 8px;
                border: 1.5px solid #BFDBFE;
            }
        """)
        result_layout = QHBoxLayout(result_frame)
        result_layout.setContentsMargins(20, 14, 20, 14)

        result_layout.addWidget(QLabel("⚡ Điện tiêu thụ:"))
        self.lbl_tieu_thu = QLabel("--- kWh")
        self.lbl_tieu_thu.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #1D4ED8;"
        )
        result_layout.addWidget(self.lbl_tieu_thu)
        result_layout.addStretch()

        lbl_note = QLabel("(Chỉ số mới − Chỉ số cũ)")
        lbl_note.setStyleSheet("font-size: 16px; color: #64748B; font-style: italic;")
        result_layout.addWidget(lbl_note)

        form_outer.addWidget(result_frame)

        # Nút hành động
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_style_tmpl = """
            QPushButton {{
                background: {bg}; color: {fg};
                border: none; border-radius: 7px;
                padding: 9px 24px; font-size: 16px;
                font-weight: 600; min-height: 38px;
            }}
            QPushButton:hover {{ background: {hover}; }}
        """
        self.btn_calc = QPushButton("📊  Tính tiêu thụ")
        self.btn_calc.setStyleSheet(btn_style_tmpl.format(bg="#3B82F6", fg="white", hover="#2563EB"))

        self.btn_save = QPushButton("💾  Lưu chỉ số")
        self.btn_save.setStyleSheet(btn_style_tmpl.format(bg="#10B981", fg="white", hover="#059669"))

        self.btn_clear = QPushButton("🗑️  Xóa form")
        self.btn_clear.setStyleSheet(btn_style_tmpl.format(bg="#6B7280", fg="white", hover="#4B5563"))

        btn_layout.addWidget(self.btn_calc)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_clear)
        form_outer.addLayout(btn_layout)

        main_layout.addWidget(form_frame)

        # ── Bảng lịch sử chỉ số ─────────────────────────────
        hist_label = QLabel("📋 Lịch sử chỉ số đã nhập")
        hist_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(hist_label)

        self.table = QTableWidget()
        columns = ["Mã KH", "Tên KH", "Tháng", "Chỉ số cũ", "Chỉ số mới", "Tiêu thụ (kWh)"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setMaximumHeight(220)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #FFFFFF; border-radius: 10px;
                border: none; font-size: 16px; color: #1E293B;
            }
            QTableWidget::item { padding: 9px 12px; border-bottom: 1px solid #F1F5F9; }
            QTableWidget::item:selected { background: #EFF6FF; color: #1D4ED8; }
            QHeaderView::section {
                background: #F8FAFC; color: #64748B;
                font-size: 16px; font-weight: bold;
                padding: 9px 12px; border: none;
                border-bottom: 2px solid #E2E8F0;
            }
            QTableWidget::item:alternate { background: #F8FAFC; }
        """)
        main_layout.addWidget(self.table)

        # Kết nối signal-slot
        self.txt_chi_so_cu.textChanged.connect(self._auto_calc)
        self.txt_chi_so_moi.textChanged.connect(self._auto_calc)
        self.btn_calc.clicked.connect(self._on_calc)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_clear.clicked.connect(self._on_clear)

    def _auto_calc(self):
        """Tự động tính tiêu thụ khi thay đổi chỉ số"""
        try:
            cu = int(self.txt_chi_so_cu.text())
            moi = int(self.txt_chi_so_moi.text())
            if moi >= cu:
                tieu_thu = moi - cu
                self.lbl_tieu_thu.setText(f"{tieu_thu} kWh")
                self.lbl_tieu_thu.setStyleSheet(
                    "font-size: 22px; font-weight: bold; color: #10B981;"
                )
            else:
                self.lbl_tieu_thu.setText("⚠ Chỉ số mới < cũ!")
                self.lbl_tieu_thu.setStyleSheet(
                    "font-size: 16px; font-weight: bold; color: #EF4444;"
                )
        except ValueError:
            self.lbl_tieu_thu.setText("--- kWh")
            self.lbl_tieu_thu.setStyleSheet(
                "font-size: 22px; font-weight: bold; color: #1D4ED8;"
            )

    def _on_calc(self):
        """Tính và hiển thị tiêu thụ"""
        self._auto_calc()

    def _on_save(self):
        """Lưu chỉ số vào danh sách"""
        try:
            cu = int(self.txt_chi_so_cu.text())
            moi = int(self.txt_chi_so_moi.text())
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Chỉ số phải là số nguyên!")
            return

        if moi < cu:
            QMessageBox.warning(self, "Lỗi", "Chỉ số mới không được nhỏ hơn chỉ số cũ!")
            return

        ma_kh = self.cmb_kh.currentData()
        ten_kh = self.cmb_kh.currentText().split(" - ", 1)[-1]
        thang = self.txt_thang.text().strip() or "04/2026"

        record = {
            "ma_kh": ma_kh,
            "ten_kh": ten_kh,
            "thang": thang,
            "chi_so_cu": cu,
            "chi_so_moi": moi,
            "tieu_thu": moi - cu,
        }
        self.readings.append(record)
        self._load_table()
        QMessageBox.information(self, "Thành công", "Đã lưu chỉ số điện!")
        print(f"[INPUT] Lưu chỉ số: {record}")

    def _on_clear(self):
        """Xóa form nhập"""
        self.txt_chi_so_cu.clear()
        self.txt_chi_so_moi.clear()
        self.lbl_tieu_thu.setText("--- kWh")
        self.lbl_tieu_thu.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #1D4ED8;"
        )

    def _load_table(self):
        """Nạp lịch sử chỉ số vào bảng"""
        self.table.setRowCount(0)
        for row_idx, r in enumerate(self.readings):
            self.table.insertRow(row_idx)
            values = [
                r["ma_kh"], r["ten_kh"], r["thang"],
                str(r["chi_so_cu"]), str(r["chi_so_moi"]),
                f"{r['tieu_thu']} kWh"
            ]
            for col_idx, text in enumerate(values):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                if col_idx == 5:
                    item.setForeground(QColor("#1D4ED8"))
                self.table.setItem(row_idx, col_idx, item)
