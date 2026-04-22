"""
views/report_view.py - Màn hình Báo cáo
Thống kê tiêu thụ điện, doanh thu theo tháng
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QPushButton,
    QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data.mock_data import CUSTOMERS, INVOICES, ELECTRICITY_READINGS, tinh_tien_dien


class ReportView(QWidget):
    """
    Màn hình Báo cáo thống kê.
    Hiển thị tổng hợp tiêu thụ điện và doanh thu theo tháng.
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
        header = QLabel("📈 Báo cáo Thống kê")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(header)

        sub = QLabel("Tháng 04/2026 | Khu dân cư")
        sub.setStyleSheet("font-size: 16px; color: #64748B; margin-top: -10px;")
        main_layout.addWidget(sub)

        # ── Thẻ KPI ─────────────────────────────────────────
        kpi_layout = QGridLayout()
        kpi_layout.setSpacing(14)

        tong_tieu_thu = sum(r["tieu_thu"] for r in ELECTRICITY_READINGS)
        tong_doanh_thu = sum(i["tong_tien"] for i in INVOICES)
        da_thanh_toan = sum(i["tong_tien"] for i in INVOICES if i["trang_thai"] == "Đã thanh toán")
        chua_thanh_toan = tong_doanh_thu - da_thanh_toan
        tb_tieu_thu = tong_tieu_thu / len(ELECTRICITY_READINGS) if ELECTRICITY_READINGS else 0

        kpis = [
            ("⚡", "Tổng điện tiêu thụ", f"{tong_tieu_thu:,} kWh", "#3B82F6"),
            ("📊", "TB tiêu thụ/hộ", f"{tb_tieu_thu:.1f} kWh", "#8B5CF6"),
            ("💰", "Tổng doanh thu", f"{tong_doanh_thu:,.0f}đ", "#10B981"),
            ("✅", "Đã thu", f"{da_thanh_toan:,.0f}đ", "#06B6D4"),
            ("⏳", "Chưa thu", f"{chua_thanh_toan:,.0f}đ", "#EF4444"),
            ("🏠", "Số hộ ghi chỉ số", str(len(ELECTRICITY_READINGS)), "#F59E0B"),
        ]

        for idx, (icon, title, value, color) in enumerate(kpis):
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: #FFFFFF; border-radius: 10px;
                    border-left: 4px solid {color};
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            card_layout.setSpacing(4)

            lbl_icon = QLabel(f"{icon}  {title}")
            lbl_icon.setStyleSheet("font-size: 16px; color: #64748B;")

            lbl_val = QLabel(value)
            lbl_val.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")

            card_layout.addWidget(lbl_icon)
            card_layout.addWidget(lbl_val)

            kpi_layout.addWidget(card, idx // 3, idx % 3)

        main_layout.addLayout(kpi_layout)

        # ── 2 bảng song song ─────────────────────────────────
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(16)

        # Bảng 1: Tiêu thụ theo khách hàng
        left = QFrame()
        left.setStyleSheet("QFrame { background: #FFFFFF; border-radius: 12px; }")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(16, 14, 16, 14)
        left_layout.setSpacing(10)

        lbl_t1 = QLabel("⚡ Điện tiêu thụ theo hộ")
        lbl_t1.setStyleSheet("font-size: 17px; font-weight: bold; color: #1E293B;")
        left_layout.addWidget(lbl_t1)

        self.table_usage = QTableWidget()
        self.table_usage.setColumnCount(4)
        self.table_usage.setHorizontalHeaderLabels(["Mã KH", "Tên KH", "Tiêu thụ (kWh)", "% Tổng"])
        self.table_usage.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._setup_table_style(self.table_usage)
        self._load_usage_table()
        left_layout.addWidget(self.table_usage)

        tables_layout.addWidget(left)

        # Bảng 2: Doanh thu / hóa đơn
        right = QFrame()
        right.setStyleSheet("QFrame { background: #FFFFFF; border-radius: 12px; }")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(16, 14, 16, 14)
        right_layout.setSpacing(10)

        lbl_t2 = QLabel("💰 Doanh thu theo hộ")
        lbl_t2.setStyleSheet("font-size: 17px; font-weight: bold; color: #1E293B;")
        right_layout.addWidget(lbl_t2)

        self.table_revenue = QTableWidget()
        self.table_revenue.setColumnCount(4)
        self.table_revenue.setHorizontalHeaderLabels(["Mã HĐ", "Tên KH", "Tổng tiền", "Trạng thái"])
        self.table_revenue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._setup_table_style(self.table_revenue)
        self._load_revenue_table()
        right_layout.addWidget(self.table_revenue)

        tables_layout.addWidget(right)
        main_layout.addLayout(tables_layout)

        # Nút xuất báo cáo (console)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_export = QPushButton("📄  Xuất báo cáo (Console)")
        btn_export.setStyleSheet("""
            QPushButton {
                background: #1E3A5F; color: white;
                border: none; border-radius: 8px;
                padding: 10px 24px; font-size: 16px;
                font-weight: 600; min-height: 40px;
            }
            QPushButton:hover { background: #1D4ED8; }
        """)
        btn_export.clicked.connect(self._on_export)
        btn_layout.addWidget(btn_export)
        main_layout.addLayout(btn_layout)

    def _setup_table_style(self, table: QTableWidget):
        """Áp dụng style chung cho bảng"""
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setMaximumHeight(250)
        table.setStyleSheet("""
            QTableWidget {
                background: #FFFFFF; border-radius: 10px;
                border: none; font-size: 16px; color: #1E293B;
            }
            QTableWidget::item { padding: 9px 10px; border-bottom: 1px solid #F1F5F9; }
            QTableWidget::item:selected { background: #EFF6FF; color: #1D4ED8; }
            QHeaderView::section {
                background: #F8FAFC; color: #64748B;
                font-size: 16px; font-weight: bold;
                padding: 9px 10px; border: none;
                border-bottom: 2px solid #E2E8F0;
            }
            QTableWidget::item:alternate { background: #F8FAFC; }
        """)

    def _load_usage_table(self):
        """Nạp bảng tiêu thụ điện"""
        from data.mock_data import ELECTRICITY_READINGS
        tong = sum(r["tieu_thu"] for r in ELECTRICITY_READINGS) or 1
        self.table_usage.setRowCount(0)

        # Sắp xếp giảm dần theo tiêu thụ
        sorted_data = sorted(ELECTRICITY_READINGS, key=lambda r: r["tieu_thu"], reverse=True)
        for row_idx, r in enumerate(sorted_data):
            self.table_usage.insertRow(row_idx)
            pct = r["tieu_thu"] / tong * 100
            for col_idx, text in enumerate([r["ma_kh"], r["ten_kh"],
                                            f"{r['tieu_thu']} kWh", f"{pct:.1f}%"]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                if col_idx == 2:
                    item.setForeground(QColor("#1D4ED8"))
                self.table_usage.setItem(row_idx, col_idx, item)

    def _load_revenue_table(self):
        """Nạp bảng doanh thu"""
        self.table_revenue.setRowCount(0)
        color_map = {"Đã thanh toán": "#10B981", "Chưa thanh toán": "#EF4444"}

        sorted_inv = sorted(INVOICES, key=lambda i: i["tong_tien"], reverse=True)
        for row_idx, inv in enumerate(sorted_inv):
            self.table_revenue.insertRow(row_idx)
            for col_idx, text in enumerate([
                inv["ma_hd"], inv["ten_kh"],
                f"{inv['tong_tien']:,.0f}đ", inv["trang_thai"]
            ]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                if col_idx == 2:
                    item.setForeground(QColor("#1D4ED8"))
                if col_idx == 3:
                    item.setForeground(QColor(color_map.get(text, "#64748B")))
                self.table_revenue.setItem(row_idx, col_idx, item)

    def _on_export(self):
        """Xuất báo cáo ra console"""
        from data.mock_data import ELECTRICITY_READINGS
        sep = "=" * 60
        print(f"\n{sep}")
        print(f"        BÁO CÁO THỐNG KÊ ĐIỆN - THÁNG 04/2026")
        print(sep)
        print(f"  {'Khách hàng':<30} {'Tiêu thụ':>12} {'Tiền điện':>15}")
        print(f"  {'-'*57}")
        for r in ELECTRICITY_READINGS:
            tien = tinh_tien_dien(r["tieu_thu"])["tong_tien"]
            print(f"  {r['ten_kh']:<30} {r['tieu_thu']:>10} kWh  {tien:>12,.0f}đ")
        tong_kwh = sum(r["tieu_thu"] for r in ELECTRICITY_READINGS)
        tong_tien = sum(tinh_tien_dien(r["tieu_thu"])["tong_tien"] for r in ELECTRICITY_READINGS)
        print(f"  {'-'*57}")
        print(f"  {'TỔNG CỘNG':<30} {tong_kwh:>10} kWh  {tong_tien:>12,.0f}đ")
        print(f"{sep}\n")
