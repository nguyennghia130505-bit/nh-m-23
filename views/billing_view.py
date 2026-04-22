"""
views/billing_view.py - Màn hình Tính Tiền Điện
Áp dụng giá bậc thang, hiển thị chi tiết tính tiền
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data.mock_data import CUSTOMERS, ELECTRICITY_READINGS, tinh_tien_dien, ELECTRICITY_TIERS


class BillingView(QWidget):
    """
    Màn hình Tính Tiền Điện theo giá bậc thang:
      - Bậc 1 (0–50 kWh): 1.500đ/kWh
      - Bậc 2 (51–100 kWh): 2.000đ/kWh
      - Bậc 3 (>100 kWh): 2.500đ/kWh
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        """Xây dựng giao diện"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("💰 Tính Tiền Điện")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(header)

        # ── Layout 2 cột ────────────────────────────────────
        content = QHBoxLayout()
        content.setSpacing(20)

        # ── Cột trái: form tính tiền ─────────────────────────
        left_panel = QFrame()
        left_panel.setMaximumWidth(420)
        left_panel.setStyleSheet("QFrame { background: #FFFFFF; border-radius: 12px; }")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 18, 20, 18)
        left_layout.setSpacing(14)

        form_title = QLabel("📋 Nhập thông tin tính tiền")
        form_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B;")
        left_layout.addWidget(form_title)

        input_style = """
            QLineEdit, QComboBox {
                border: 1.5px solid #E2E8F0;
                border-radius: 7px;
                padding: 8px 12px;
                font-size: 17px;
                background: #F8FAFC;
                min-height: 40px;
            }
            QLineEdit:focus, QComboBox:focus { border-color: #3B82F6; }
        """
        label_style = "font-size: 16px; font-weight: 600; color: #374151; margin-top: 4px;"

        # Chọn khách hàng
        lbl_kh = QLabel("Chọn khách hàng:")
        lbl_kh.setStyleSheet(label_style)
        self.cmb_kh = QComboBox()
        self.cmb_kh.setStyleSheet(input_style)
        self.cmb_kh.addItem("-- Chọn khách hàng --", userData=None)
        for c in CUSTOMERS:
            self.cmb_kh.addItem(f"{c['ma_kh']} - {c['ten']}", userData=c["ma_kh"])
        self.cmb_kh.currentIndexChanged.connect(self._on_customer_selected)

        left_layout.addWidget(lbl_kh)
        left_layout.addWidget(self.cmb_kh)

        # Điện tiêu thụ
        lbl_tt = QLabel("Điện tiêu thụ (kWh):")
        lbl_tt.setStyleSheet(label_style)
        self.txt_tieu_thu = QLineEdit()
        self.txt_tieu_thu.setPlaceholderText("Nhập số kWh hoặc chọn KH có dữ liệu...")
        self.txt_tieu_thu.setStyleSheet(input_style)
        self.txt_tieu_thu.textChanged.connect(self._on_kwh_changed)

        left_layout.addWidget(lbl_tt)
        left_layout.addWidget(self.txt_tieu_thu)

        # Bảng giá bậc thang (tham khảo)
        lbl_bac = QLabel("📊 Bảng giá bậc thang:")
        lbl_bac.setStyleSheet(label_style)
        left_layout.addWidget(lbl_bac)

        for tier in ELECTRICITY_TIERS:
            tier_row = QFrame()
            tier_row.setStyleSheet("QFrame { background: #F8FAFC; border-radius: 6px; }")
            tier_h = QHBoxLayout(tier_row)
            tier_h.setContentsMargins(12, 6, 12, 6)
            lbl_name = QLabel(tier["mo_ta"])
            lbl_name.setStyleSheet("font-size: 16px; color: #374151;")
            lbl_price = QLabel(f"{tier['don_gia']:,}đ/kWh")
            lbl_price.setStyleSheet("font-size: 16px; font-weight: bold; color: #1D4ED8;")
            tier_h.addWidget(lbl_name)
            tier_h.addStretch()
            tier_h.addWidget(lbl_price)
            left_layout.addWidget(tier_row)

        # Nút tính tiền
        self.btn_calc = QPushButton("⚡  Tính tiền điện")
        self.btn_calc.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                color: white; border: none; border-radius: 8px;
                padding: 10px; font-size: 17px;
                font-weight: bold; min-height: 42px;
            }
            QPushButton:hover { background: #2563EB; }
        """)
        self.btn_calc.clicked.connect(self._on_calc)
        left_layout.addWidget(self.btn_calc)
        left_layout.addStretch()

        content.addWidget(left_panel)

        # ── Cột phải: kết quả tính tiền ─────────────────────
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { background: #FFFFFF; border-radius: 12px; }")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 18, 20, 18)
        right_layout.setSpacing(14)

        result_title = QLabel("📄 Chi tiết tính tiền")
        result_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B;")
        right_layout.addWidget(result_title)

        # Tên khách hàng
        self.lbl_kh_name = QLabel("Chưa chọn khách hàng")
        self.lbl_kh_name.setStyleSheet("font-size: 17px; color: #64748B;")
        right_layout.addWidget(self.lbl_kh_name)

        # Bảng chi tiết
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Bậc", "Số kWh", "Đơn giá", "Thành tiền"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setShowGrid(False)
        self.result_table.setMaximumHeight(180)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setStyleSheet("""
            QTableWidget {
                background: #FFFFFF; border-radius: 10px;
                border: 1px solid #E2E8F0; font-size: 16px;
            }
            QTableWidget::item { padding: 9px 12px; border-bottom: 1px solid #F1F5F9; }
            QHeaderView::section {
                background: #F8FAFC; color: #64748B;
                font-size: 16px; font-weight: bold;
                padding: 9px 12px; border: none;
                border-bottom: 2px solid #E2E8F0;
            }
            QTableWidget::item:alternate { background: #F8FAFC; }
        """)
        right_layout.addWidget(self.result_table)

        # Tổng tiền nổi bật
        total_frame = QFrame()
        total_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1E3A5F, stop:1 #1D4ED8);
                border-radius: 10px;
            }
        """)
        total_layout = QHBoxLayout(total_frame)
        total_layout.setContentsMargins(20, 16, 20, 16)

        lbl_total_text = QLabel("TỔNG TIỀN ĐIỆN:")
        lbl_total_text.setStyleSheet("font-size: 17px; color: #BFDBFE; font-weight: 600;")
        total_layout.addWidget(lbl_total_text)
        total_layout.addStretch()

        self.lbl_total = QLabel("0 đồng")
        self.lbl_total.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #F59E0B;"
        )
        total_layout.addWidget(self.lbl_total)

        right_layout.addWidget(total_frame)
        right_layout.addStretch()

        content.addWidget(right_panel)
        main_layout.addLayout(content)

    def _on_customer_selected(self, index: int):
        """Khi chọn khách hàng, tự điền tiêu thụ nếu có dữ liệu"""
        ma_kh = self.cmb_kh.currentData()
        if not ma_kh:
            self.lbl_kh_name.setText("Chưa chọn khách hàng")
            return

        # Tìm tên khách hàng
        kh_text = self.cmb_kh.currentText().split(" - ", 1)
        self.lbl_kh_name.setText(f"Khách hàng: {kh_text[-1]}" if len(kh_text) > 1 else "")

        # Tìm chỉ số tiêu thụ gần nhất
        record = next(
            (r for r in ELECTRICITY_READINGS if r["ma_kh"] == ma_kh),
            None
        )
        if record:
            self.txt_tieu_thu.setText(str(record["tieu_thu"]))

    def _on_kwh_changed(self):
        """Xóa kết quả khi thay đổi input"""
        self.result_table.setRowCount(0)
        self.lbl_total.setText("0 đồng")

    def _on_calc(self):
        """Tính tiền điện và hiển thị kết quả"""
        try:
            kwh = int(self.txt_tieu_thu.text())
            if kwh < 0:
                raise ValueError
        except ValueError:
            self.lbl_total.setText("⚠ Số kWh không hợp lệ!")
            self.lbl_total.setStyleSheet("font-size: 16px; font-weight: bold; color: #EF4444;")
            return

        result = tinh_tien_dien(kwh)

        # Hiển thị chi tiết bảng
        self.result_table.setRowCount(0)
        for row_idx, item in enumerate(result["chi_tiet"]):
            self.result_table.insertRow(row_idx)
            row_vals = [
                item["bac"],
                f"{item['so_kwh']} kWh",
                f"{item['don_gia']:,}đ/kWh",
                f"{item['thanh_tien']:,}đ",
            ]
            for col_idx, text in enumerate(row_vals):
                cell = QTableWidgetItem(text)
                cell.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                if col_idx == 3:
                    cell.setForeground(QColor("#1D4ED8"))
                self.result_table.setItem(row_idx, col_idx, cell)

        # Hiển thị tổng
        tong = result["tong_tien"]
        self.lbl_total.setText(f"{tong:,.0f} đồng")
        self.lbl_total.setStyleSheet("font-size: 24px; font-weight: bold; color: #F59E0B;")
        print(f"[BILLING] {kwh} kWh → {tong:,}đ")
