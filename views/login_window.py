"""
views/login_window.py - Cửa sổ đăng nhập
"""

import os
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from data.mock_data import USERS


class LoginWindow(QDialog):
    """
    Cửa sổ đăng nhập hệ thống.
    Phát signal login_success khi đăng nhập thành công.
    """
    login_success = pyqtSignal(str)  # Signal mang tên username

    def __init__(self, parent=None):
        super().__init__(parent)
        # Load giao diện từ file .ui
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "login.ui")
        uic.loadUi(ui_path, self)

        # Ẩn tiêu đề hệ thống (dùng custom frame)
        self.setWindowFlag(0x00000800, False)  # Bỏ help button

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Thiết lập giao diện ban đầu"""
        # Set style cho icon
        self.lblIcon.setStyleSheet("font-size: 56px; color: #F59E0B;")
        self.lblTitle.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #1E3A5F; letter-spacing: 1px;"
        )
        self.lblSubtitle.setStyleSheet("font-size: 16px; color: #64748B;")
        self.lblError.setStyleSheet("color: #EF4444; font-size: 15px;")
        self.lblHint.setStyleSheet("color: #94A3B8; font-size: 15px; font-style: italic;")

        # Style cho input fields
        input_style = """
            QLineEdit {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                padding: 12px 18px;
                font-size: 17px;
                background: #F8FAFC;
                color: #1E293B;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                background: #FFFFFF;
            }
        """
        self.txtUsername.setStyleSheet(input_style)
        self.txtPassword.setStyleSheet(input_style)

        # Style cho nút đăng nhập
        self.btnLogin.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 17px;
                font-weight: bold;
                letter-spacing: 1px;
                min-height: 54px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563EB, stop:1 #1E40AF);
            }
            QPushButton:pressed {
                background: #1D4ED8;
            }
        """)

        # Label cho form fields
        label_style = "font-size: 16px; font-weight: 600; color: #374151;"
        self.lblUsername.setStyleSheet(label_style)
        self.lblPassword.setStyleSheet(label_style)

        # Màu nền dialog
        self.setStyleSheet("QDialog { background: #FFFFFF; }")

    def _connect_signals(self):
        """Kết nối các signal-slot"""
        self.btnLogin.clicked.connect(self._on_login_clicked)
        # Nhấn Enter trong ô password cũng đăng nhập
        self.txtPassword.returnPressed.connect(self._on_login_clicked)
        self.txtUsername.returnPressed.connect(lambda: self.txtPassword.setFocus())

    def _on_login_clicked(self):
        """Xử lý sự kiện bấm nút Đăng nhập"""
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text()

        # Validate form đơn giản
        if not username:
            self.lblError.setText("⚠ Vui lòng nhập tên đăng nhập!")
            self.txtUsername.setFocus()
            return
        if not password:
            self.lblError.setText("⚠ Vui lòng nhập mật khẩu!")
            self.txtPassword.setFocus()
            return

        # Kiểm tra thông tin đăng nhập
        if username in USERS and USERS[username]["password"] == password:
            self.lblError.setText("")
            print(f"[LOGIN] Đăng nhập thành công: {username}")
            self.login_success.emit(username)
            self.accept()  # Đóng dialog, trả về Accepted
        else:
            self.lblError.setText("✗ Tên đăng nhập hoặc mật khẩu không đúng!")
            self.txtPassword.clear()
            self.txtPassword.setFocus()
