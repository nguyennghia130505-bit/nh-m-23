import pymysql
from pymysql import Error

class DBConnection:
    """Quản lý kết nối tới MySQL (XAMPP) bằng PyMySQL siêu nhẹ"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """Mở kết nối tới MySQL"""
        try:
            if self.connection is None or not self.connection.open:
                self.connection = pymysql.connect(
                    host='localhost',
                    database='dien_khu_dan_cu',
                    user='root',
                    password=''
                )
                print("[DB] Đã kết nối tới MySQL: dien_khu_dan_cu")
            return self.connection
        except Error as e:
            print(f"[DB_ERROR] Lỗi kết nối MySQL: {e}")
            return None

    def close(self):
        """Đóng kết nối"""
        if self.connection and self.connection.open:
            self.connection.close()
            print("[DB] Đã đóng kết nối MySQL.")

def get_connection():
    """Hàm helper để lấy connection object"""
    return DBConnection().connect()
