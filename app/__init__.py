# Flask app 模組初始化
import sqlite3
import os

def init_db():
    """
    初始化資料庫。讀取 database/schema.sql 並在 instance/database.db 中建立資料表。
    """
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')
    
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
        print("資料庫初始化成功！")
    except Exception as e:
        print(f"資料庫初始化失敗: {e}")
