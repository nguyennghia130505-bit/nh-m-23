"""
data/mock_data.py - Dữ liệu giả lập cho toàn bộ ứng dụng
"""

# ============================================================
# Dữ liệu khách hàng (hộ dân)
# ============================================================
CUSTOMERS = [
    {"ma_kh": "KH001", "ten": "Nguyễn Văn An", "dia_chi": "12 Lý Tự Trọng, P.1, Q.1", "sdt": "0901234567", "trang_thai": "Đang hoạt động"},
    {"ma_kh": "KH002", "ten": "Trần Thị Bình", "dia_chi": "45 Nguyễn Huệ, P.2, Q.1", "sdt": "0912345678", "trang_thai": "Đang hoạt động"},
    {"ma_kh": "KH003", "ten": "Lê Minh Cường", "dia_chi": "78 Hai Bà Trưng, P.3, Q.3", "sdt": "0923456789", "trang_thai": "Đang hoạt động"},
    {"ma_kh": "KH004", "ten": "Phạm Thị Dung", "dia_chi": "23 Đinh Tiên Hoàng, P.4, Q.Bình Thạnh", "sdt": "0934567890", "trang_thai": "Tạm ngừng"},
    {"ma_kh": "KH005", "ten": "Hoàng Văn Em", "dia_chi": "56 Lê Văn Sỹ, P.12, Q.3", "sdt": "0945678901", "trang_thai": "Đang hoạt động"},
    {"ma_kh": "KH006", "ten": "Vũ Thị Phương", "dia_chi": "89 Cách Mạng Tháng 8, P.5, Q.Tân Bình", "sdt": "0956789012", "trang_thai": "Đang hoạt động"},
    {"ma_kh": "KH007", "ten": "Đặng Quốc Hùng", "dia_chi": "34 Nam Kỳ Khởi Nghĩa, P.7, Q.3", "sdt": "0967890123", "trang_thai": "Đang hoạt động"},
    {"ma_kh": "KH008", "ten": "Bùi Thị Lan", "dia_chi": "67 Trần Phú, P.8, Q.5", "sdt": "0978901234", "trang_thai": "Đang hoạt động"},
]

# ============================================================
# Dữ liệu công tơ điện
# ============================================================
METERS = [
    {"ma_cong_to": "CT001", "ma_kh": "KH001", "ten_kh": "Nguyễn Văn An", "vi_tri": "Cột điện A1", "trang_thai": "Hoạt động"},
    {"ma_cong_to": "CT002", "ma_kh": "KH002", "ten_kh": "Trần Thị Bình", "vi_tri": "Cột điện A2", "trang_thai": "Hoạt động"},
    {"ma_cong_to": "CT003", "ma_kh": "KH003", "ten_kh": "Lê Minh Cường", "vi_tri": "Cột điện B1", "trang_thai": "Hoạt động"},
    {"ma_cong_to": "CT004", "ma_kh": "KH004", "ten_kh": "Phạm Thị Dung", "vi_tri": "Cột điện B2", "trang_thai": "Hỏng"},
    {"ma_cong_to": "CT005", "ma_kh": "KH005", "ten_kh": "Hoàng Văn Em", "vi_tri": "Cột điện C1", "trang_thai": "Hoạt động"},
    {"ma_cong_to": "CT006", "ma_kh": "KH006", "ten_kh": "Vũ Thị Phương", "vi_tri": "Cột điện C2", "trang_thai": "Hoạt động"},
    {"ma_cong_to": "CT007", "ma_kh": "KH007", "ten_kh": "Đặng Quốc Hùng", "vi_tri": "Cột điện D1", "trang_thai": "Hoạt động"},
    {"ma_cong_to": "CT008", "ma_kh": "KH008", "ten_kh": "Bùi Thị Lan", "vi_tri": "Cột điện D2", "trang_thai": "Hoạt động"},
]

# ============================================================
# Dữ liệu chỉ số điện theo tháng
# ============================================================
ELECTRICITY_READINGS = [
    {"ma_kh": "KH001", "ten_kh": "Nguyễn Văn An", "thang": "04/2026", "chi_so_cu": 1200, "chi_so_moi": 1285, "tieu_thu": 85},
    {"ma_kh": "KH002", "ten_kh": "Trần Thị Bình", "thang": "04/2026", "chi_so_cu": 800, "chi_so_moi": 860, "tieu_thu": 60},
    {"ma_kh": "KH003", "ten_kh": "Lê Minh Cường", "thang": "04/2026", "chi_so_cu": 2100, "chi_so_moi": 2245, "tieu_thu": 145},
    {"ma_kh": "KH005", "ten_kh": "Hoàng Văn Em", "thang": "04/2026", "chi_so_cu": 450, "chi_so_moi": 498, "tieu_thu": 48},
    {"ma_kh": "KH006", "ten_kh": "Vũ Thị Phương", "thang": "04/2026", "chi_so_cu": 1500, "chi_so_moi": 1620, "tieu_thu": 120},
]

# ============================================================
# Dữ liệu hóa đơn (tháng hiện tại)
# ============================================================
INVOICES = [
    {"ma_hd": "HD001", "ma_kh": "KH001", "ten_kh": "Nguyễn Văn An", "thang": "04/2026", "tieu_thu": 85, "tong_tien": 147500, "trang_thai": "Chưa thanh toán"},
    {"ma_hd": "HD002", "ma_kh": "KH002", "ten_kh": "Trần Thị Bình", "thang": "04/2026", "tieu_thu": 60, "tong_tien": 107500, "trang_thai": "Đã thanh toán"},
    {"ma_hd": "HD003", "ma_kh": "KH003", "ten_kh": "Lê Minh Cường", "thang": "04/2026", "tieu_thu": 145, "tong_tien": 286250, "trang_thai": "Chưa thanh toán"},
    {"ma_hd": "HD004", "ma_kh": "KH005", "ten_kh": "Hoàng Văn Em", "thang": "04/2026", "tieu_thu": 48, "tong_tien": 72000, "trang_thai": "Đã thanh toán"},
    {"ma_hd": "HD005", "ma_kh": "KH006", "ten_kh": "Vũ Thị Phương", "thang": "04/2026", "tieu_thu": 120, "tong_tien": 232500, "trang_thai": "Chưa thanh toán"},
]

# ============================================================
# Lịch sử hóa đơn đa tháng (dùng cho màn hình Đã Thanh Toán)
# ============================================================
INVOICES_HISTORY = [
    # ── Tháng 01/2026 ─────────────────────────────────────
    {"ma_hd": "H2601001", "ma_kh": "KH001", "ten_kh": "Nguyễn Văn An",    "dia_chi": "12 Lý Tự Trọng, P.1, Q.1",            "thang": "01/2026", "tieu_thu": 78,  "tong_tien": 131000,  "trang_thai": "Đã thanh toán", "ngay_tt": "05/01/2026"},
    {"ma_hd": "H2601002", "ma_kh": "KH002", "ten_kh": "Trần Thị Bình",   "dia_chi": "45 Nguyễn Huệ, P.2, Q.1",             "thang": "01/2026", "tieu_thu": 55,  "tong_tien": 97500,   "trang_thai": "Đã thanh toán", "ngay_tt": "07/01/2026"},
    {"ma_hd": "H2601003", "ma_kh": "KH003", "ten_kh": "Lê Minh Cường",   "dia_chi": "78 Hai Bà Trưng, P.3, Q.3",           "thang": "01/2026", "tieu_thu": 130, "tong_tien": 257500,  "trang_thai": "Đã thanh toán", "ngay_tt": "08/01/2026"},
    {"ma_hd": "H2601004", "ma_kh": "KH005", "ten_kh": "Hoàng Văn Em",    "dia_chi": "56 Lê Văn Sỹ, P.12, Q.3",             "thang": "01/2026", "tieu_thu": 42,  "tong_tien": 63000,   "trang_thai": "Đã thanh toán", "ngay_tt": "10/01/2026"},
    {"ma_hd": "H2601005", "ma_kh": "KH006", "ten_kh": "Vũ Thị Phương",   "dia_chi": "89 Cách Mạng Tháng 8, P.5, Q.Tân Bình", "thang": "01/2026", "tieu_thu": 110, "tong_tien": 207500,  "trang_thai": "Đã thanh toán", "ngay_tt": "12/01/2026"},
    {"ma_hd": "H2601006", "ma_kh": "KH007", "ten_kh": "Đặng Quốc Hùng",  "dia_chi": "34 Nam Kỳ Khởi Nghĩa, P.7, Q.3",       "thang": "01/2026", "tieu_thu": 95,  "tong_tien": 172500,  "trang_thai": "Đã thanh toán", "ngay_tt": "14/01/2026"},
    {"ma_hd": "H2601007", "ma_kh": "KH008", "ten_kh": "Bùi Thị Lan",     "dia_chi": "67 Trần Phú, P.8, Q.5",               "thang": "01/2026", "tieu_thu": 63,  "tong_tien": 114500,  "trang_thai": "Đã thanh toán", "ngay_tt": "15/01/2026"},
    # ── Tháng 02/2026 ─────────────────────────────────────
    {"ma_hd": "H2602001", "ma_kh": "KH001", "ten_kh": "Nguyễn Văn An",    "dia_chi": "12 Lý Tự Trọng, P.1, Q.1",            "thang": "02/2026", "tieu_thu": 82,  "tong_tien": 139000,  "trang_thai": "Đã thanh toán", "ngay_tt": "06/02/2026"},
    {"ma_hd": "H2602002", "ma_kh": "KH002", "ten_kh": "Trần Thị Bình",   "dia_chi": "45 Nguyễn Huệ, P.2, Q.1",             "thang": "02/2026", "tieu_thu": 58,  "tong_tien": 103500,  "trang_thai": "Đã thanh toán", "ngay_tt": "08/02/2026"},
    {"ma_hd": "H2602003", "ma_kh": "KH003", "ten_kh": "Lê Minh Cường",   "dia_chi": "78 Hai Bà Trưng, P.3, Q.3",           "thang": "02/2026", "tieu_thu": 140, "tong_tien": 277500,  "trang_thai": "Đã thanh toán", "ngay_tt": "10/02/2026"},
    {"ma_hd": "H2602004", "ma_kh": "KH005", "ten_kh": "Hoàng Văn Em",    "dia_chi": "56 Lê Văn Sỹ, P.12, Q.3",             "thang": "02/2026", "tieu_thu": 45,  "tong_tien": 67500,   "trang_thai": "Chưa thanh toán", "ngay_tt": ""},
    {"ma_hd": "H2602005", "ma_kh": "KH006", "ten_kh": "Vũ Thị Phương",   "dia_chi": "89 Cách Mạng Tháng 8, P.5, Q.Tân Bình", "thang": "02/2026", "tieu_thu": 115, "tong_tien": 220000,  "trang_thai": "Đã thanh toán", "ngay_tt": "11/02/2026"},
    {"ma_hd": "H2602006", "ma_kh": "KH007", "ten_kh": "Đặng Quốc Hùng",  "dia_chi": "34 Nam Kỳ Khởi Nghĩa, P.7, Q.3",       "thang": "02/2026", "tieu_thu": 88,  "tong_tien": 160000,  "trang_thai": "Đã thanh toán", "ngay_tt": "13/02/2026"},
    {"ma_hd": "H2602007", "ma_kh": "KH008", "ten_kh": "Bùi Thị Lan",     "dia_chi": "67 Trần Phú, P.8, Q.5",               "thang": "02/2026", "tieu_thu": 70,  "tong_tien": 127500,  "trang_thai": "Chưa thanh toán", "ngay_tt": ""},
    # ── Tháng 03/2026 ─────────────────────────────────────
    {"ma_hd": "H2603001", "ma_kh": "KH001", "ten_kh": "Nguyễn Văn An",    "dia_chi": "12 Lý Tự Trọng, P.1, Q.1",            "thang": "03/2026", "tieu_thu": 90,  "tong_tien": 157500,  "trang_thai": "Đã thanh toán", "ngay_tt": "04/03/2026"},
    {"ma_hd": "H2603002", "ma_kh": "KH002", "ten_kh": "Trần Thị Bình",   "dia_chi": "45 Nguyễn Huệ, P.2, Q.1",             "thang": "03/2026", "tieu_thu": 62,  "tong_tien": 112000,  "trang_thai": "Đã thanh toán", "ngay_tt": "06/03/2026"},
    {"ma_hd": "H2603003", "ma_kh": "KH003", "ten_kh": "Lê Minh Cường",   "dia_chi": "78 Hai Bà Trưng, P.3, Q.3",           "thang": "03/2026", "tieu_thu": 155, "tong_tien": 307500,  "trang_thai": "Đã thanh toán", "ngay_tt": "07/03/2026"},
    {"ma_hd": "H2603004", "ma_kh": "KH005", "ten_kh": "Hoàng Văn Em",    "dia_chi": "56 Lê Văn Sỹ, P.12, Q.3",             "thang": "03/2026", "tieu_thu": 50,  "tong_tien": 75000,   "trang_thai": "Đã thanh toán", "ngay_tt": "09/03/2026"},
    {"ma_hd": "H2603005", "ma_kh": "KH006", "ten_kh": "Vũ Thị Phương",   "dia_chi": "89 Cách Mạng Tháng 8, P.5, Q.Tân Bình", "thang": "03/2026", "tieu_thu": 118, "tong_tien": 225000,  "trang_thai": "Chưa thanh toán", "ngay_tt": ""},
    {"ma_hd": "H2603006", "ma_kh": "KH007", "ten_kh": "Đặng Quốc Hùng",  "dia_chi": "34 Nam Kỳ Khởi Nghĩa, P.7, Q.3",       "thang": "03/2026", "tieu_thu": 100, "tong_tien": 182500,  "trang_thai": "Đã thanh toán", "ngay_tt": "11/03/2026"},
    {"ma_hd": "H2603007", "ma_kh": "KH008", "ten_kh": "Bùi Thị Lan",     "dia_chi": "67 Trần Phú, P.8, Q.5",               "thang": "03/2026", "tieu_thu": 68,  "tong_tien": 123000,  "trang_thai": "Đã thanh toán", "ngay_tt": "12/03/2026"},
    # ── Tháng 04/2026 ─────────────────────────────────────
    {"ma_hd": "HD001",    "ma_kh": "KH001", "ten_kh": "Nguyễn Văn An",    "dia_chi": "12 Lý Tự Trọng, P.1, Q.1",            "thang": "04/2026", "tieu_thu": 85,  "tong_tien": 147500,  "trang_thai": "Chưa thanh toán", "ngay_tt": ""},
    {"ma_hd": "HD002",    "ma_kh": "KH002", "ten_kh": "Trần Thị Bình",   "dia_chi": "45 Nguyễn Huệ, P.2, Q.1",             "thang": "04/2026", "tieu_thu": 60,  "tong_tien": 107500,  "trang_thai": "Đã thanh toán", "ngay_tt": "18/04/2026"},
    {"ma_hd": "HD003",    "ma_kh": "KH003", "ten_kh": "Lê Minh Cường",   "dia_chi": "78 Hai Bà Trưng, P.3, Q.3",           "thang": "04/2026", "tieu_thu": 145, "tong_tien": 286250,  "trang_thai": "Chưa thanh toán", "ngay_tt": ""},
    {"ma_hd": "HD004",    "ma_kh": "KH005", "ten_kh": "Hoàng Văn Em",    "dia_chi": "56 Lê Văn Sỹ, P.12, Q.3",             "thang": "04/2026", "tieu_thu": 48,  "tong_tien": 72000,   "trang_thai": "Đã thanh toán", "ngay_tt": "20/04/2026"},
    {"ma_hd": "HD005",    "ma_kh": "KH006", "ten_kh": "Vũ Thị Phương",   "dia_chi": "89 Cách Mạng Tháng 8, P.5, Q.Tân Bình", "thang": "04/2026", "tieu_thu": 120, "tong_tien": 232500,  "trang_thai": "Chưa thanh toán", "ngay_tt": ""},
]

# ============================================================
# Bảng giá điện bậc thang (VNĐ/kWh)
# ============================================================
ELECTRICITY_TIERS = [
    {"bac": "Bậc 1", "tu": 0, "den": 50, "don_gia": 1500, "mo_ta": "0 - 50 kWh"},
    {"bac": "Bậc 2", "tu": 51, "den": 100, "don_gia": 2000, "mo_ta": "51 - 100 kWh"},
    {"bac": "Bậc 3", "tu": 101, "den": float('inf'), "don_gia": 2500, "mo_ta": "> 100 kWh"},
]

# ============================================================
# Thông tin đăng nhập (giả lập)
# ============================================================
USERS = {
    "admin": {"password": "123", "ho_ten": "Quản trị viên", "role": "admin"},
    "nhanvien": {"password": "abc", "ho_ten": "Nhân Viên A", "role": "staff"},
}


def tinh_tien_dien(so_kwh: int) -> dict:
    """
    Tính tiền điện theo giá bậc thang
    Args:
        so_kwh: Số kWh tiêu thụ
    Returns:
        dict: Chi tiết tính tiền theo từng bậc và tổng tiền
    """
    chi_tiet = []
    tong_tien = 0

    if so_kwh <= 0:
        return {"chi_tiet": [], "tong_tien": 0}

    # Bậc 1: 0 - 50 kWh → 1.500đ/kWh
    bac1 = min(so_kwh, 50)
    phi_bac1 = bac1 * 1500
    tong_tien += phi_bac1
    chi_tiet.append({"bac": "Bậc 1 (0-50 kWh)", "so_kwh": bac1, "don_gia": 1500, "thanh_tien": phi_bac1})

    # Bậc 2: 51 - 100 kWh → 2.000đ/kWh
    if so_kwh > 50:
        bac2 = min(so_kwh - 50, 50)
        phi_bac2 = bac2 * 2000
        tong_tien += phi_bac2
        chi_tiet.append({"bac": "Bậc 2 (51-100 kWh)", "so_kwh": bac2, "don_gia": 2000, "thanh_tien": phi_bac2})

    # Bậc 3: >100 kWh → 2.500đ/kWh
    if so_kwh > 100:
        bac3 = so_kwh - 100
        phi_bac3 = bac3 * 2500
        tong_tien += phi_bac3
        chi_tiet.append({"bac": "Bậc 3 (>100 kWh)", "so_kwh": bac3, "don_gia": 2500, "thanh_tien": phi_bac3})

    return {"chi_tiet": chi_tiet, "tong_tien": tong_tien}
