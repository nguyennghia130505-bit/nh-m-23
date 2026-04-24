import pymysql
from data.db_connection import get_connection

# =====================================================================
# USERS
# =====================================================================
def verify_login(username, password):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        return cursor.fetchone()
    finally:
        cursor.close()

def get_user(username):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()
    finally:
        cursor.close()

# =====================================================================
# CUSTOMERS
# =====================================================================
def get_all_customers():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT ma_kh, ten, dia_chi, sdt, trang_thai FROM customers")
        return cursor.fetchall()
    finally:
        cursor.close()

def add_customer(data):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (ma_kh, ten, dia_chi, sdt, trang_thai) VALUES (%s, %s, %s, %s, %s)",
            (data['ma_kh'], data['ten'], data['dia_chi'], data['sdt'], data['trang_thai'])
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] add_customer: {e}")
        return False
    finally:
        cursor.close()

def update_customer(ma_kh, data):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE customers SET ten=%s, dia_chi=%s, sdt=%s, trang_thai=%s WHERE ma_kh=%s",
            (data['ten'], data['dia_chi'], data['sdt'], data['trang_thai'], ma_kh)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] update_customer: {e}")
        return False
    finally:
        cursor.close()

def delete_customer(ma_kh):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE ma_kh=%s", (ma_kh,))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] delete_customer: {e}")
        return False
    finally:
        cursor.close()

# =====================================================================
# METERS
# =====================================================================
def get_all_meters():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT m.ma_cong_to, m.ma_kh, c.ten as ten_kh, m.vi_tri, m.trang_thai 
            FROM meters m 
            LEFT JOIN customers c ON m.ma_kh = c.ma_kh
        """)
        return cursor.fetchall()
    finally:
        cursor.close()

def add_meter(data):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO meters (ma_cong_to, ma_kh, vi_tri, trang_thai) VALUES (%s, %s, %s, %s)",
            (data['ma_cong_to'], data['ma_kh'], data['vi_tri'], data['trang_thai'])
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] add_meter: {e}")
        return False
    finally:
        cursor.close()

def update_meter(ma_cong_to, data):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE meters SET ma_kh=%s, vi_tri=%s, trang_thai=%s WHERE ma_cong_to=%s",
            (data['ma_kh'], data['vi_tri'], data['trang_thai'], ma_cong_to)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] update_meter: {e}")
        return False
    finally:
        cursor.close()

def delete_meter(ma_cong_to):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM meters WHERE ma_cong_to=%s", (ma_cong_to,))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] delete_meter: {e}")
        return False
    finally:
        cursor.close()

# =====================================================================
# ELECTRICITY READINGS
# =====================================================================
def get_all_readings():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT r.*, c.ten as ten_kh 
            FROM electricity_readings r 
            LEFT JOIN customers c ON r.ma_kh = c.ma_kh
        """)
        return cursor.fetchall()
    finally:
        cursor.close()

def get_latest_reading(ma_cong_to):
    """Lấy chỉ số mới nhất của một công tơ (để tự điền chỉ số cũ)"""
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT * FROM electricity_readings 
            WHERE ma_cong_to = %s 
            ORDER BY id DESC LIMIT 1
        """, (ma_cong_to,))
        return cursor.fetchone()
    finally:
        cursor.close()

def add_reading(data):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO electricity_readings (ma_kh, ma_cong_to, thang, chi_so_cu, chi_so_moi, tieu_thu) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['ma_kh'], data['ma_cong_to'], data['thang'], data['chi_so_cu'], data['chi_so_moi'], data['tieu_thu'])
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] add_reading: {e}")
        return False
    finally:
        cursor.close()

# =====================================================================
# INVOICES
# =====================================================================
def get_all_invoices():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT i.*, c.ten as ten_kh, c.dia_chi 
            FROM invoices i 
            LEFT JOIN customers c ON i.ma_kh = c.ma_kh
            ORDER BY i.ma_hd DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()

def get_invoices_history():
    """Tương đương với INVOICES_HISTORY cũ"""
    return get_all_invoices()

def add_invoice(data):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO invoices (ma_hd, ma_kh, ma_cong_to, thang, tieu_thu, tong_tien, trang_thai, ngay_tt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (data['ma_hd'], data['ma_kh'], data['ma_cong_to'], data['thang'], data['tieu_thu'], data['tong_tien'], data['trang_thai'], data.get('ngay_tt', ''))
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] add_invoice: {e}")
        return False
    finally:
        cursor.close()

def update_invoice_status(ma_hd, trang_thai, ngay_tt=""):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE invoices SET trang_thai=%s, ngay_tt=%s WHERE ma_hd=%s",
            (trang_thai, ngay_tt, ma_hd)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] update_invoice_status: {e}")
        return False
    finally:
        cursor.close()

# =====================================================================
# BILLING CALCULATION
# =====================================================================
def get_electricity_tiers():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM electricity_tiers ORDER BY tu ASC")
        return cursor.fetchall()
    finally:
        cursor.close()

def tinh_tien_dien_db(so_kwh: int) -> dict:
    tiers = get_electricity_tiers()
    if not tiers: return {"chi_tiet": [], "tong_tien": 0}
    
    chi_tiet = []
    tong_tien = 0
    kwh_con_lai = so_kwh

    for i, t in enumerate(tiers):
        if kwh_con_lai <= 0:
            break
            
        gioi_han = t["den"] - t["tu"] + 1
        
        # Bậc cuối cùng (den thường rất lớn ví dụ 999999)
        if i == len(tiers) - 1:
            gioi_han = float('inf')

        kwh_bac = min(kwh_con_lai, gioi_han)
        tien_bac = kwh_bac * t["don_gia"]

        chi_tiet.append({
            "bac": t["bac"],
            "so_kwh": int(kwh_bac),
            "don_gia": t["don_gia"],
            "thanh_tien": int(tien_bac)
        })

        tong_tien += tien_bac
        kwh_con_lai -= kwh_bac

    return {
        "chi_tiet": chi_tiet,
        "tong_tien": int(tong_tien)
    }
