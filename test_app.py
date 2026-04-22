"""
test_app.py - Script kiểm tra toàn bộ ứng dụng (headless)
Chạy: python test_app.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

print("=== TEST SUITE: Quan ly Dien Khu Dan Cu ===")

# Test 1: Import tất cả views
print("[1] Import views...")
from views.login_window import LoginWindow
from views.main_window import MainWindow
from views.dashboard_view import DashboardView
from views.customer_view import CustomerView
from views.meter_view import MeterView
from views.electricity_input_view import ElectricityInputView
from views.billing_view import BillingView
from views.invoice_view import InvoiceView
from views.report_view import ReportView
print("    OK - All views imported")

# Test 2: MainWindow khởi tạo
print("[2] MainWindow creation...")
mw = MainWindow('admin')
assert mw.stackedWidget.count() == 7, "Expected 7 pages"
print(f"    OK - {mw.stackedWidget.count()} pages loaded")

# Test 3: Navigation
print("[3] Navigation test...")
for i in range(7):
    mw.menuList.setCurrentRow(i)
    assert mw.stackedWidget.currentIndex() == i, f"Failed nav index {i}"
print("    OK - All 7 navigation slots work")

# Test 4: Billing logic
print("[4] Billing logic...")
from data.mock_data import tinh_tien_dien
r = tinh_tien_dien(50)    # Bac 1 only: 50*1500 = 75000
assert r['tong_tien'] == 75000, f"Expected 75000, got {r['tong_tien']}"
r = tinh_tien_dien(80)    # Bac 1: 50*1500=75000, Bac 2: 30*2000=60000 => 135000
assert r['tong_tien'] == 135000, f"Expected 135000, got {r['tong_tien']}"
r = tinh_tien_dien(120)   # Bac 1+2: 225000, Bac 3: 20*2500=50000 => 225000+50000=275000... wait
# Bac1: 50*1500=75000, Bac2: 50*2000=100000, Bac3: 20*2500=50000 => 225000
assert r['tong_tien'] == 225000, f"Expected 225000, got {r['tong_tien']}"
print("    OK - Tiered billing calculation correct")

# Test 5: Data integrity
print("[5] Data integrity...")
from data.mock_data import CUSTOMERS, METERS, INVOICES, ELECTRICITY_READINGS
assert len(CUSTOMERS) == 8
assert len(METERS) == 8
assert len(INVOICES) == 5
assert len(ELECTRICITY_READINGS) == 5
print(f"    OK - {len(CUSTOMERS)} KH, {len(METERS)} cong to, {len(INVOICES)} hoa don")

# Test 6: Customer CRUD simulation
print("[6] Customer CRUD simulation...")
import copy
customers = copy.deepcopy(CUSTOMERS)
new_kh = {"ma_kh": "KH099", "ten": "Test Nguoi", "dia_chi": "123 Test", "sdt": "0999999999", "trang_thai": "Dang hoat dong"}
customers.append(new_kh)
assert len(customers) == 9
customers = [c for c in customers if c["ma_kh"] != "KH099"]
assert len(customers) == 8
print("    OK - Add/delete customer simulation works")

print("")
print("=== ALL TESTS PASSED! App is ready to run. ===")
print("")
print("Chay ung dung: python main.py")
