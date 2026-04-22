"""
views/customer_view.py - Màn hình Quản lý Khách hàng
CRUD operations: Thêm, Sửa, Xóa, Tìm kiếm khách hàng
"""

import copy
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QFrame, QMessageBox, QDialog,
    QFormLayout, QDialogButtonBox, QHeaderView,
    QAbstractItemView, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data.mock_data import CUSTOMERS


class CustomerFormDialog(QDialog):
    """Dialog thêm/sửa thông tin khách hàng"""

    def __init__(self, data: dict = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm khách hàng" if data is None else "Sửa khách hàng")
        self.setFixedSize(420, 350)
        self.setStyleSheet("QDialog { background: #FFFFFF; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("📋 " + self.windowTitle())
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E293B;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        input_style = """
            QLineEdit, QComboBox {
                border: 1.5px solid #E2E8F0;
                border-radius: 6px;
                padding: 7px 10px;
                font-size: 16px;
                background: #F8FAFC;
                min-height: 32px;
            }
            QLineEdit:focus, QComboBox:focus { border-color: #3B82F6; }
        """
        label_style = "font-size: 16px; font-weight: 600; color: #374151;"

        # Các trường nhập liệu
        self.txt_ma = QLineEdit()
        self.txt_ten = QLineEdit()
        self.txt_dia_chi = QLineEdit()
        self.txt_sdt = QLineEdit()
        self.cmb_trang_thai = QComboBox()
        self.cmb_trang_thai.addItems(["Đang hoạt động", "Tạm ngừng"])

        for w in [self.txt_ma, self.txt_ten, self.txt_dia_chi, self.txt_sdt, self.cmb_trang_thai]:
            w.setStyleSheet(input_style)

        lbl_ma = QLabel("Mã KH:")
        lbl_ten = QLabel("Họ tên:")
        lbl_dc = QLabel("Địa chỉ:")
        lbl_sdt = QLabel("SĐT:")
        lbl_tt = QLabel("Trạng thái:")
        for lbl in [lbl_ma, lbl_ten, lbl_dc, lbl_sdt, lbl_tt]:
            lbl.setStyleSheet(label_style)

        form.addRow(lbl_ma, self.txt_ma)
        form.addRow(lbl_ten, self.txt_ten)
        form.addRow(lbl_dc, self.txt_dia_chi)
        form.addRow(lbl_sdt, self.txt_sdt)
        form.addRow(lbl_tt, self.cmb_trang_thai)
        layout.addLayout(form)

        # Nếu có data (chế độ sửa) thì điền sẵn
        if data:
            self.txt_ma.setText(data.get("ma_kh", ""))
            self.txt_ma.setReadOnly(True)  # Không cho sửa mã KH
            self.txt_ten.setText(data.get("ten", ""))
            self.txt_dia_chi.setText(data.get("dia_chi", ""))
            self.txt_sdt.setText(data.get("sdt", ""))
            idx = self.cmb_trang_thai.findText(data.get("trang_thai", ""))
            if idx >= 0:
                self.cmb_trang_thai.setCurrentIndex(idx)

        # Buttons OK/Cancel
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.setStyleSheet("""
            QPushButton {
                min-width: 90px; min-height: 34px;
                border-radius: 6px; font-size: 16px; font-weight: 600;
            }
            QPushButton[text="OK"] { background: #3B82F6; color: white; border: none; }
            QPushButton[text="OK"]:hover { background: #2563EB; }
            QPushButton[text="Cancel"] { background: #F1F5F9; color: #374151; border: 1px solid #E2E8F0; }
        """)
        btn_box.accepted.connect(self._validate_and_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _validate_and_accept(self):
        """Validate form trước khi đóng dialog"""
        if not self.txt_ma.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã KH!")
            return
        if not self.txt_ten.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Họ tên!")
            return
        self.accept()

    def get_data(self) -> dict:
        """Trả về dữ liệu từ form"""
        return {
            "ma_kh": self.txt_ma.text().strip(),
            "ten": self.txt_ten.text().strip(),
            "dia_chi": self.txt_dia_chi.text().strip(),
            "sdt": self.txt_sdt.text().strip(),
            "trang_thai": self.cmb_trang_thai.currentText(),
        }


class CustomerView(QWidget):
    """
    Màn hình Quản lý Khách hàng.
    Hỗ trợ: Thêm, Sửa, Xóa, Tìm kiếm.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Tạo bản sao dữ liệu mock để không ảnh hưởng nguồn gốc
        self.customers = copy.deepcopy(CUSTOMERS)
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        """Xây dựng giao diện"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # ── Header ──────────────────────────────────────────
        header = QLabel("👥 Quản lý Khách hàng")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        main_layout.addWidget(header)

        # ── Toolbar (tìm kiếm + nút hành động) ──────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Ô tìm kiếm
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍  Tìm kiếm theo tên, mã KH, SĐT...")
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

        # Nút hành động
        btn_style = """
            QPushButton {{
                background: {bg};
                color: {fg};
                border: none;
                border-radius: 7px;
                padding: 8px 18px;
                font-size: 16px;
                font-weight: 600;
                min-height: 36px;
            }}
            QPushButton:hover {{ background: {hover}; }}
        """
        self.btn_add = QPushButton("➕  Thêm")
        self.btn_add.setStyleSheet(btn_style.format(bg="#3B82F6", fg="white", hover="#2563EB"))

        self.btn_edit = QPushButton("✏️  Sửa")
        self.btn_edit.setStyleSheet(btn_style.format(bg="#F59E0B", fg="white", hover="#D97706"))

        self.btn_delete = QPushButton("🗑️  Xóa")
        self.btn_delete.setStyleSheet(btn_style.format(bg="#EF4444", fg="white", hover="#DC2626"))

        self.btn_refresh = QPushButton("🔄  Làm mới")
        self.btn_refresh.setStyleSheet(btn_style.format(bg="#6B7280", fg="white", hover="#4B5563"))

        for btn in [self.btn_add, self.btn_edit, self.btn_delete, self.btn_refresh]:
            toolbar.addWidget(btn)

        main_layout.addLayout(toolbar)

        # ── Bảng dữ liệu ────────────────────────────────────
        self.table = QTableWidget()
        columns = ["Mã KH", "Họ tên", "Địa chỉ", "Số điện thoại", "Trạng thái"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 80)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 130)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 130)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #FFFFFF;
                border-radius: 10px;
                border: none;
                gridline-color: #F1F5F9;
                font-size: 16px;
                color: #1E293B;
            }
            QTableWidget::item {
                padding: 10px 12px;
                border-bottom: 1px solid #F1F5F9;
            }
            QTableWidget::item:selected {
                background: #EFF6FF;
                color: #1D4ED8;
            }
            QHeaderView::section {
                background: #F8FAFC;
                color: #64748B;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 12px;
                border: none;
                border-bottom: 2px solid #E2E8F0;
            }
            QTableWidget::item:alternate {
                background: #F8FAFC;
            }
        """)
        main_layout.addWidget(self.table)

        # ── Thanh trạng thái ─────────────────────────────────
        self.lbl_count = QLabel("Tổng: 0 khách hàng")
        self.lbl_count.setStyleSheet("font-size: 11px; color: #64748B;")
        main_layout.addWidget(self.lbl_count)

        # Kết nối signal-slot
        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_refresh.clicked.connect(self._on_refresh)
        self.table.doubleClicked.connect(self._on_edit)

    def _load_table(self, data: list = None):
        """Nạp dữ liệu vào bảng"""
        if data is None:
            data = self.customers

        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            items = [
                row_data["ma_kh"],
                row_data["ten"],
                row_data["dia_chi"],
                row_data["sdt"],
                row_data["trang_thai"],
            ]
            for col_idx, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                # Tô màu trạng thái
                if col_idx == 4:
                    if text == "Đang hoạt động":
                        item.setForeground(QColor("#10B981"))
                    else:
                        item.setForeground(QColor("#EF4444"))
                self.table.setItem(row_idx, col_idx, item)

        self.lbl_count.setText(f"Tổng: {len(data)} khách hàng")

    def _on_search(self, keyword: str):
        """Lọc bảng theo từ khóa tìm kiếm"""
        keyword = keyword.lower().strip()
        if not keyword:
            self._load_table()
            return
        filtered = [
            c for c in self.customers
            if keyword in c["ma_kh"].lower()
            or keyword in c["ten"].lower()
            or keyword in c["sdt"]
        ]
        self._load_table(filtered)

    def _get_selected_customer(self):
        """Trả về dict dữ liệu khách hàng đang được chọn"""
        row = self.table.currentRow()
        if row < 0:
            return None
        ma_kh = self.table.item(row, 0).text()
        return next((c for c in self.customers if c["ma_kh"] == ma_kh), None)

    def _on_add(self):
        """Mở dialog thêm khách hàng"""
        dialog = CustomerFormDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.get_data()
            # Kiểm tra trùng mã KH
            if any(c["ma_kh"] == new_data["ma_kh"] for c in self.customers):
                QMessageBox.warning(self, "Lỗi", f"Mã KH '{new_data['ma_kh']}' đã tồn tại!")
                return
            self.customers.append(new_data)
            self._load_table()
            QMessageBox.information(self, "Thành công", "Thêm khách hàng thành công!")
            print(f"[CUSTOMER] Thêm: {new_data}")

    def _on_edit(self):
        """Mở dialog sửa khách hàng"""
        cust = self._get_selected_customer()
        if cust is None:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một khách hàng để sửa!")
            return
        dialog = CustomerFormDialog(data=cust, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            updated = dialog.get_data()
            # Cập nhật lại danh sách
            for i, c in enumerate(self.customers):
                if c["ma_kh"] == updated["ma_kh"]:
                    self.customers[i] = updated
                    break
            self._load_table()
            QMessageBox.information(self, "Thành công", "Cập nhật thành công!")
            print(f"[CUSTOMER] Sửa: {updated}")

    def _on_delete(self):
        """Xóa khách hàng đang chọn"""
        cust = self._get_selected_customer()
        if cust is None:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một khách hàng để xóa!")
            return
        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc muốn xóa khách hàng '{cust['ten']}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.customers = [c for c in self.customers if c["ma_kh"] != cust["ma_kh"]]
            self._load_table()
            print(f"[CUSTOMER] Xóa: {cust['ma_kh']}")

    def _on_refresh(self):
        """Làm mới bảng, xóa tìm kiếm"""
        self.txt_search.clear()
        self._load_table()
