import pymysql

def upgrade_db():
    conn = pymysql.connect(
        host='localhost',
        database='dien_khu_dan_cu',
        user='root',
        password=''
    )
    cursor = conn.cursor()
    
    queries = [
        # Bảng electricity_readings
        "ALTER TABLE electricity_readings ADD COLUMN ma_cong_to varchar(20) NOT NULL AFTER ma_kh;",
        # Bảng invoices
        "ALTER TABLE invoices ADD COLUMN ma_cong_to varchar(20) NOT NULL AFTER ma_kh;"
    ]
    
    for q in queries:
        try:
            cursor.execute(q)
            print(f"Thành công: {q}")
        except Exception as e:
            print(f"Bỏ qua (có thể đã tồn tại): {q} - Lỗi: {e}")
            
    # Update dữ liệu cũ: Lấy công tơ đầu tiên của KH gán cho readings và invoices cũ
    try:
        cursor.execute("SELECT ma_kh, ma_cong_to FROM meters")
        meters = cursor.fetchall()
        for m in meters:
            ma_kh = m[0]
            ma_cong_to = m[1]
            cursor.execute("UPDATE electricity_readings SET ma_cong_to = %s WHERE ma_kh = %s AND ma_cong_to = ''", (ma_cong_to, ma_kh))
            cursor.execute("UPDATE invoices SET ma_cong_to = %s WHERE ma_kh = %s AND ma_cong_to = ''", (ma_cong_to, ma_kh))
        print("Đã cập nhật dữ liệu mã công tơ cho các bản ghi cũ.")
    except Exception as e:
        print(f"Lỗi cập nhật dữ liệu: {e}")
        
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    upgrade_db()
