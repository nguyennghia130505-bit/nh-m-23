"""
views/dashboard_view.py - Màn hình Dashboard tổng quan
Hiển thị thống kê nhanh và thông tin tổng quan hệ thống
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data.mock_data import CUSTOMERS, METERS, INVOICES, ELECTRICITY_READINGS


class StatCard(QFrame):
    """Widget card thống kê nhỏ gọn"""

    def __init__(self, icon: str, title: str, value: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        # Icon
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet(f"font-size: 28px;")

        # Value
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(
            f"font-size: 28px; font-weight: bold; color: {color};"
        )

        # Title
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 16px; color: #64748B;")

        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_value)
        layout.addWidget(lbl_title)
        layout.addStretch()

        self.setStyleSheet(f"""
            QFrame#statCard {{
                background: #FFFFFF;
                border-radius: 12px;
                border-left: 4px solid {color};
            }}
            QFrame#statCard:hover {{
                background: #F8FAFC;
            }}
        """)


class DashboardView(QWidget):
    """
    Màn hình Dashboard tổng quan.
    Hiển thị các thẻ thống kê và bảng tóm tắt hóa đơn gần đây.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        """Xây dựng giao diện dashboard"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(20)

        # ── Header ──────────────────────────────────────────
        header = QLabel("📊 Dashboard - Tổng quan hệ thống")
        header.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #1E293B;"
        )
        main_layout.addWidget(header)

        sub = QLabel("Thống kê dịch vụ cung cấp điện khu dân cư")
        sub.setStyleSheet("font-size: 17px; color: #64748B; margin-top: -10px;")
        main_layout.addWidget(sub)

        # ── Thẻ thống kê ────────────────────────────────────
        card_grid = QGridLayout()
        card_grid.setSpacing(16)

        tong_kh = len(CUSTOMERS)
        kh_hoat_dong = sum(1 for c in CUSTOMERS if c["trang_thai"] == "Đang hoạt động")
        cong_to_hong = sum(1 for m in METERS if m["trang_thai"] == "Hỏng")
        hd_chua_tt = sum(1 for i in INVOICES if i["trang_thai"] == "Chưa thanh toán")
        tong_doanh_thu = sum(i["tong_tien"] for i in INVOICES if i["trang_thai"] == "Đã thanh toán")

        cards = [
            ("👥", "Tổng khách hàng", str(tong_kh), "#3B82F6"),
            ("✅", "Đang hoạt động", str(kh_hoat_dong), "#10B981"),
            ("⚡", "Công tơ lỗi", str(cong_to_hong), "#EF4444"),
            ("🧾", "HĐ chưa thanh toán", str(hd_chua_tt), "#F59E0B"),
            ("💰", "Doanh thu tháng", f"{tong_doanh_thu:,.0f}đ", "#8B5CF6"),
            ("📋", "Chỉ số đã nhập", str(len(ELECTRICITY_READINGS)), "#06B6D4"),
        ]

        for i, (icon, title, value, color) in enumerate(cards):
            card = StatCard(icon, title, value, color)
            card_grid.addWidget(card, i // 3, i % 3)

        main_layout.addLayout(card_grid)

        # ── Hóa đơn gần đây ─────────────────────────────────
        recent_label = QLabel("🕐 Hóa đơn gần đây")
        recent_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #1E293B; margin-top: 8px;"
        )
        main_layout.addWidget(recent_label)

        # Bảng tóm tắt (dùng QFrame + label thay vì QTableWidget để nhẹ hơn)
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border-radius: 12px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        # Tiêu đề bảng
        header_row = QWidget()
        header_row.setStyleSheet("background: #F1F5F9; border-radius: 10px 10px 0 0;")
        header_h = QHBoxLayout(header_row)
        header_h.setContentsMargins(16, 10, 16, 10)
        for col_name, width in [("Mã HĐ", 80), ("Khách hàng", 200), ("Tháng", 80),
                                 ("Điện tiêu thụ", 120), ("Tổng tiền", 150), ("Trạng thái", 150)]:
            lbl = QLabel(col_name)
            lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #64748B;")
            lbl.setFixedWidth(width)
            header_h.addWidget(lbl)
        header_h.addStretch()
        table_layout.addWidget(header_row)

        # Dữ liệu
        colors_tt = {"Đã thanh toán": "#10B981", "Chưa thanh toán": "#EF4444"}
        for idx, inv in enumerate(INVOICES):
            row = QWidget()
            bg = "#FFFFFF" if idx % 2 == 0 else "#F8FAFC"
            row.setStyleSheet(f"background: {bg};")
            row_h = QHBoxLayout(row)
            row_h.setContentsMargins(16, 10, 16, 10)

            data = [
                (inv["ma_hd"], 80, "#1E293B"),
                (inv["ten_kh"], 200, "#1E293B"),
                (inv["thang"], 80, "#64748B"),
                (f"{inv['tieu_thu']} kWh", 120, "#64748B"),
                (f"{inv['tong_tien']:,.0f}đ", 150, "#1D4ED8"),
                (inv["trang_thai"], 150, colors_tt.get(inv["trang_thai"], "#64748B")),
            ]
            for text, width, color in data:
                lbl = QLabel(text)
                lbl.setStyleSheet(f"font-size: 16px; color: {color};")
                lbl.setFixedWidth(width)
                row_h.addWidget(lbl)
            row_h.addStretch()
            table_layout.addWidget(row)

        main_layout.addWidget(table_frame)
        main_layout.addStretch()
