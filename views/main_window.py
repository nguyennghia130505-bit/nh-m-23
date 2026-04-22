"""
views/main_window.py - Cửa sổ chính của ứng dụng
Chứa sidebar điều hướng và QStackedWidget để hiển thị các màn hình con
"""

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

from data.mock_data import USERS
from views.dashboard_view import DashboardView
from views.customer_view import CustomerView
from views.meter_view import MeterView
from views.electricity_input_view import ElectricityInputView
from views.billing_view import BillingView
from views.invoice_view import InvoiceView
from views.report_view import ReportView


# Ánh xạ chỉ số menu → index trong QStackedWidget
MENU_INDEX = {
    0: "Dashboard",
    1: "Khách hàng",
    2: "Công tơ",
    3: "Nhập chỉ số",
    4: "Tính tiền",
    5: "Hóa đơn",
    6: "Báo cáo",
}


class MainWindow(QMainWindow):
    """
    Cửa sổ chính với sidebar và StackedWidget.
    Mỗi mục menu tương ứng một page trong stacked widget.
    """

    def __init__(self, username: str = "admin", parent=None):
        super().__init__(parent)
        self.username = username

        # Load giao diện từ file .ui
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "main_window.ui")
        uic.loadUi(ui_path, self)

        self._apply_styles()
        self._init_pages()
        self._connect_signals()

        # Chọn mục đầu tiên mặc định (Dashboard)
        self.menuList.setCurrentRow(0)

        # Cập nhật tên user trên sidebar
        ho_ten = USERS.get(username, {}).get("ho_ten", username)
        self.lblUser.setText(f"👤 {ho_ten}")

        self.statusbar.showMessage(f"Đã đăng nhập: {ho_ten}  |  Hệ thống Quản lý Điện Khu Dân Cư")

    def _apply_styles(self):
        """Áp dụng stylesheet cho cửa sổ chính"""
        self.setStyleSheet("""
            QMainWindow {
                background: #F1F5F9;
            }
        """)

        # Sidebar
        self.sidebar.setStyleSheet("""
            QFrame#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1E3A5F, stop:1 #0F2744);
            }
        """)

        # Header sidebar
        self.sidebarHeader.setStyleSheet("""
            QFrame#sidebarHeader {
                background: rgba(255,255,255,0.07);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
        """)

        self.lblAppIcon.setStyleSheet("font-size: 36px; color: #F59E0B;")
        self.lblAppName.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #FFFFFF; padding: 2px 0;"
        )
        self.lblUser.setStyleSheet("font-size: 15px; color: #94A3B8; padding-bottom: 4px;")

        # Menu list
        self.menuList.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                outline: none;
                padding: 8px 0;
            }
            QListWidget::item {
                color: #CBD5E1;
                font-size: 17px;
                padding: 18px 24px;
                border-left: 3px solid transparent;
                margin: 6px 0;
            }
            QListWidget::item:hover {
                background: rgba(255,255,255,0.08);
                color: #FFFFFF;
            }
            QListWidget::item:selected {
                background: rgba(59,130,246,0.25);
                color: #FFFFFF;
                border-left: 3px solid #3B82F6;
                font-weight: bold;
            }
        """)

        # Nút đăng xuất
        self.btnLogout.setStyleSheet("""
            QPushButton#btnLogout {
                background: rgba(239,68,68,0.15);
                color: #FCA5A5;
                border: none;
                border-top: 1px solid rgba(255,255,255,0.1);
                font-size: 17px;
                text-align: left;
                padding: 14px 20px;
            }
            QPushButton#btnLogout:hover {
                background: rgba(239,68,68,0.3);
                color: #FFFFFF;
            }
        """)

        # Status bar
        self.statusbar.setStyleSheet(
            "background: #1E3A5F; color: #94A3B8; font-size: 14px;"
        )

    def _init_pages(self):
        """Khởi tạo và thêm tất cả các trang vào QStackedWidget"""
        self.dashboard_page = DashboardView()
        self.customer_page = CustomerView()
        self.meter_page = MeterView()
        self.electricity_input_page = ElectricityInputView()
        self.billing_page = BillingView()
        self.invoice_page = InvoiceView()
        self.report_page = ReportView()

        # Thêm các trang theo thứ tự tương ứng với menu
        self.stackedWidget.addWidget(self.dashboard_page)       # index 0
        self.stackedWidget.addWidget(self.customer_page)        # index 1
        self.stackedWidget.addWidget(self.meter_page)           # index 2
        self.stackedWidget.addWidget(self.electricity_input_page)  # index 3
        self.stackedWidget.addWidget(self.billing_page)         # index 4
        self.stackedWidget.addWidget(self.invoice_page)         # index 5
        self.stackedWidget.addWidget(self.report_page)          # index 6

    def _connect_signals(self):
        """Kết nối signal-slot"""
        self.menuList.currentRowChanged.connect(self._on_menu_changed)
        self.btnLogout.clicked.connect(self._on_logout)

    def _on_menu_changed(self, index: int):
        """Chuyển trang khi chọn menu"""
        if 0 <= index < self.stackedWidget.count():
            self.stackedWidget.setCurrentIndex(index)
            page_name = MENU_INDEX.get(index, "")
            print(f"[NAV] Chuyển đến: {page_name}")

    def _on_logout(self):
        """Xử lý đăng xuất"""
        reply = QMessageBox.question(
            self, "Đăng xuất",
            "Bạn có chắc muốn đăng xuất?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            print("[LOGOUT] Người dùng đã đăng xuất")
            self.close()
            # Import lại LoginWindow để mở lại
            from views.login_window import LoginWindow
            login = LoginWindow()
            login.login_success.connect(self._reopen_main)
            login.exec_()

    def _reopen_main(self, username: str):
        """Mở lại MainWindow sau khi đăng nhập lại"""
        self.__init__(username)
        self.show()
