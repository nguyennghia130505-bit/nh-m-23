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

from data.db_repository import get_all_customers, get_all_meters, get_all_invoices, get_all_readings, get_invoices_history


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

        customers = get_all_customers()
        meters = get_all_meters()
        invoices = get_all_invoices()
        readings = get_all_readings()

        tong_kh = len(customers)
        kh_hoat_dong = sum(1 for c in customers if c["trang_thai"] == "Đang hoạt động")
        cong_to_hong = sum(1 for m in meters if m["trang_thai"] == "Hỏng")
        hd_chua_tt = sum(1 for i in invoices if i["trang_thai"] == "Chưa thanh toán")
        tong_doanh_thu = sum(i["tong_tien"] for i in invoices if i["trang_thai"] == "Đã thanh toán")

        cards = [
            ("👥", "Tổng khách hàng", str(tong_kh), "#3B82F6"),
            ("✅", "Đang hoạt động", str(kh_hoat_dong), "#10B981"),
            ("⚡", "Công tơ lỗi", str(cong_to_hong), "#EF4444"),
            ("🧾", "HĐ chưa thanh toán", str(hd_chua_tt), "#F59E0B"),
            ("💰", "Doanh thu tháng", f"{tong_doanh_thu:,.0f}đ", "#8B5CF6"),
            ("📋", "Chỉ số đã nhập", str(len(readings)), "#06B6D4"),
        ]

        for i, (icon, title, value, color) in enumerate(cards):
            card = StatCard(icon, title, value, color)
            card_grid.addWidget(card, i // 3, i % 3)

        main_layout.addLayout(card_grid)

        # ── Nội dung phía dưới (2 cột) ─────────────────────────
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # ── Cột trái: Hóa đơn gần đây
        recent_frame = QFrame()
        recent_layout = QVBoxLayout(recent_frame)
        recent_layout.setContentsMargins(0, 0, 0, 0)
        
        recent_label = QLabel("🕐 Hóa đơn gần đây")
        recent_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E293B; margin-top: 8px;")
        recent_layout.addWidget(recent_label)

        # Bảng tóm tắt (dùng QFrame + label thay vì QTableWidget để nhẹ hơn)
        table_frame = QFrame()
        table_frame.setStyleSheet("QFrame { background: #FFFFFF; border-radius: 12px; }")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        # Tiêu đề bảng
        header_row = QWidget()
        header_row.setStyleSheet("background: #F1F5F9; border-radius: 10px 10px 0 0;")
        header_h = QHBoxLayout(header_row)
        header_h.setContentsMargins(16, 10, 16, 10)
        for col_name, width in [("Mã HĐ", 80), ("Mã CT", 80), ("Khách hàng", 120), ("Tháng", 80),
                                 ("Tiêu thụ", 90), ("Tổng tiền", 110), ("Trạng thái", 110)]:
            lbl = QLabel(col_name)
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #64748B;")
            lbl.setFixedWidth(width)
            header_h.addWidget(lbl)
        header_h.addStretch()
        table_layout.addWidget(header_row)

        # Dữ liệu hóa đơn hiện tại
        colors_tt = {"Đã thanh toán": "#10B981", "Chưa thanh toán": "#EF4444"}
        for idx, inv in enumerate(invoices[:5]):  # Hiển thị 5 cái
            row = QWidget()
            bg = "#FFFFFF" if idx % 2 == 0 else "#F8FAFC"
            row.setStyleSheet(f"background: {bg};")
            row_h = QHBoxLayout(row)
            row_h.setContentsMargins(16, 10, 16, 10)

            data = [
                (inv["ma_hd"], 80, "#1E293B"),
                (inv.get("ma_cong_to", ""), 80, "#1E293B"),
                (inv["ten_kh"], 120, "#1E293B"),
                (inv["thang"], 80, "#64748B"),
                (f"{inv['tieu_thu']} kWh", 90, "#64748B"),
                (f"{inv['tong_tien']:,.0f}đ", 110, "#1D4ED8"),
                (inv["trang_thai"], 110, colors_tt.get(inv["trang_thai"], "#64748B")),
            ]
            for text, width, color in data:
                lbl = QLabel(text)
                lbl.setStyleSheet(f"font-size: 15px; color: {color};")
                lbl.setFixedWidth(width)
                row_h.addWidget(lbl)
            row_h.addStretch()
            table_layout.addWidget(row)

        recent_layout.addWidget(table_frame)
        recent_layout.addStretch()
        bottom_layout.addWidget(recent_frame, stretch=2)

        # ── Cột phải: Biểu đồ cột thống kê ─────────────────────
        chart_frame = QFrame()
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header Biểu đồ + Chú thích (Legend)
        chart_header_layout = QHBoxLayout()
        chart_label = QLabel("📈 Biểu đồ Doanh thu")
        chart_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E293B; margin-top: 8px;")
        chart_header_layout.addWidget(chart_label)
        
        chart_header_layout.addStretch()
        
        # Legend Đã thu
        leg_p = QFrame()
        leg_p.setFixedSize(14, 14)
        leg_p.setStyleSheet("background: #3B82F6; border-radius: 3px; margin-top: 8px;")
        chart_header_layout.addWidget(leg_p)
        lbl_leg_p = QLabel("Đã thu")
        lbl_leg_p.setStyleSheet("font-size: 14px; color: #64748B; margin-top: 8px;")
        chart_header_layout.addWidget(lbl_leg_p)
        
        # Legend Chưa thu
        leg_u = QFrame()
        leg_u.setFixedSize(14, 14)
        leg_u.setStyleSheet("background: #FCA5A5; border-radius: 3px; margin-left: 12px; margin-top: 8px;")
        chart_header_layout.addWidget(leg_u)
        lbl_leg_u = QLabel("Chưa thu")
        lbl_leg_u.setStyleSheet("font-size: 14px; color: #64748B; margin-top: 8px;")
        chart_header_layout.addWidget(lbl_leg_u)
        
        chart_layout.addLayout(chart_header_layout)
        
        chart_bg = QFrame()
        chart_bg.setStyleSheet("background: #FFFFFF; border-radius: 12px; padding: 15px 10px;")
        cb_layout = QVBoxLayout(chart_bg)
        
        bars_layout = QHBoxLayout()
        bars_layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        bars_layout.setSpacing(25)
        
        # Tính toán doanh thu Đã thu và Chưa thu theo tháng
        monthly_paid = {}
        monthly_unpaid = {}
        
        invoices_history = get_invoices_history()
        for inv in invoices_history:
            m = inv["thang"]
            if m not in monthly_paid:
                monthly_paid[m] = 0
                monthly_unpaid[m] = 0
                
            if inv["trang_thai"] == "Đã thanh toán":
                monthly_paid[m] += inv["tong_tien"]
            else:
                monthly_unpaid[m] += inv["tong_tien"]
                
        # Sắp xếp các tháng và vẽ cột dạng Stacked Bar
        sorted_months = sorted(monthly_paid.keys())
        max_total = max((monthly_paid[m] + monthly_unpaid[m]) for m in sorted_months) if sorted_months else 1
        
        for m in sorted_months:
            paid = monthly_paid[m]
            unpaid = monthly_unpaid[m]
            total = paid + unpaid
            
            col_vbox = QVBoxLayout()
            col_vbox.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            col_vbox.setSpacing(0)
            
            # Giá trị Tổng doanh thu trên đỉnh cột
            val_text = f"{total/1000000:.1f}M" if total >= 1000000 else f"{total/1000:,.0f}k"
            lbl_val = QLabel(val_text)
            lbl_val.setStyleSheet("font-size: 14px; color: #1E293B; font-weight: bold; margin-bottom: 6px;")
            lbl_val.setAlignment(Qt.AlignCenter)
            col_vbox.addWidget(lbl_val)
            
            h_unpaid = int((unpaid / max_total) * 160) if max_total > 0 else 0
            h_paid = int((paid / max_total) * 160) if max_total > 0 else 0
            
            # Khung Chưa thanh toán (màu đỏ nhạt, nằm trên)
            if h_unpaid > 0:
                bar_u = QFrame()
                # Bo tròn góc trên
                bar_u.setStyleSheet("background: #FCA5A5; border-radius: 6px; border-bottom-left-radius: 0; border-bottom-right-radius: 0;")
                bar_u.setFixedWidth(40)
                bar_u.setFixedHeight(max(5, h_unpaid))
                bar_u.setToolTip(f"Tháng {m}\nChưa thu: {unpaid:,.0f}đ")
                col_vbox.addWidget(bar_u)
                
            # Khung Đã thanh toán (màu xanh dương, nằm dưới)
            if h_paid > 0:
                bar_p = QFrame()
                # Nếu không có phần chưa thu thì phần đã thu được bo tròn ở trên
                rad_top = "6px" if h_unpaid == 0 else "0px"
                bar_p.setStyleSheet(f"background: #3B82F6; border-radius: 6px; border-top-left-radius: {rad_top}; border-top-right-radius: {rad_top};")
                bar_p.setFixedWidth(40)
                bar_p.setFixedHeight(max(10, h_paid))
                bar_p.setToolTip(f"Tháng {m}\nĐã thu: {paid:,.0f}đ")
                col_vbox.addWidget(bar_p)
            
            # Nhãn tháng ở dưới đáy
            month_num = m.split('/')[0] # Chỉ lấy số tháng
            lbl_m = QLabel(f"Thg {month_num}")
            lbl_m.setStyleSheet("font-size: 14px; color: #64748B; font-weight: bold; margin-top: 8px;")
            lbl_m.setAlignment(Qt.AlignCenter)
            col_vbox.addWidget(lbl_m)
            
            bars_layout.addLayout(col_vbox)
            
        cb_layout.addLayout(bars_layout)
        chart_layout.addWidget(chart_bg)
        chart_layout.addStretch()
        
        bottom_layout.addWidget(chart_frame, stretch=1)
        
        # Thêm toàn bộ phần dưới vào layout chính
        main_layout.addLayout(bottom_layout)
