import pymysql
import os

def setup_db():
    conn = pymysql.connect(host='localhost', user='root', password='')
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS dien_khu_dan_cu")
    cursor.execute("CREATE DATABASE dien_khu_dan_cu CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    cursor.execute("USE dien_khu_dan_cu")
    
    with open('d:/BTlPython/database.sql', 'r', encoding='utf-8') as f:
        sql_file = f.read()
    
    # Very basic SQL split
    sql_commands = sql_file.split(';')
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)
    
    conn.commit()
    conn.close()
    print("Database recreated successfully.")

if __name__ == "__main__":
    setup_db()
