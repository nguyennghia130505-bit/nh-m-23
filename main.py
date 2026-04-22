"""
main.py - Điểm khởi động ứng dụng
Hệ thống Quản lý Dịch vụ Cung cấp Điện Khu Dân Cư
"""

import sys
import os

# Thêm thư mục gốc vào sys.path để import các module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from views.login_window import LoginWindow


# Biến toàn cục giữ tham chiếu MainWindow (tránh bị garbage-collect)
_main_window = None


def open_main_window(username: str):
    """
    Callback khi đăng nhập thành công.
    Mở MainWindow với thông tin người dùng.
    """
    global _main_window
    from views.main_window import MainWindow
    _main_window = MainWindow(username=username)
    _main_window.show()
    print(f"[APP] Mở MainWindow cho user: {username}")


def main():
    """Hàm khởi động ứng dụng chính"""
    app = QApplication(sys.argv)
    app.setApplicationName("Quản lý Điện Khu Dân Cư")
    app.setOrganizationName("ElectricMgmt")

    # Đặt font mặc định cho toàn ứng dụng
    font = QFont("Segoe UI", 15)
    app.setFont(font)

    # Áp dụng stylesheet toàn ứng dụng
    qss_path = os.path.join(os.path.dirname(__file__), "resources", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("[INFO] Không tìm thấy style.qss, dùng style mặc định")

    # Hiển thị cửa sổ đăng nhập
    login = LoginWindow()

    # Kết nối signal: khi đăng nhập thành công → mở MainWindow
    login.login_success.connect(open_main_window)

    login.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

