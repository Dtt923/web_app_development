import sqlite3
import os

# 定義資料庫路徑
DATABASE_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    """
    建立並回傳與 SQLite 資料庫的連線。
    設定 row_factory 為 sqlite3.Row 以便透過欄位名稱存取資料。
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"資料庫連線錯誤: {e}")
        raise

class Task:
    @staticmethod
    def create(data):
        """
        新增一筆任務記錄。
        參數 data 為包含 title, description, due_date 的字典。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO tasks (title, description, due_date)
                VALUES (?, ?, ?)
                ''',
                (data.get('title'), data.get('description'), data.get('due_date'))
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"新增任務錯誤: {e}")
            return False

    @staticmethod
    def get_all():
        """
        取得所有任務記錄，依據建立時間反向排序。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            tasks = cursor.fetchall()
            conn.close()
            return tasks
        except sqlite3.Error as e:
            print(f"取得所有任務錯誤: {e}")
            return []

    @staticmethod
    def get_by_id(task_id):
        """
        根據 ID 取得單筆任務記錄。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            conn.close()
            return task
        except sqlite3.Error as e:
            print(f"取得單筆任務錯誤: {e}")
            return None

    @staticmethod
    def update(task_id, data):
        """
        更新特定 ID 的任務記錄。
        參數 data 包含要更新的欄位字典。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            update_fields = []
            parameters = []
            for key, value in data.items():
                if key in ['title', 'description', 'due_date', 'is_completed']:
                    update_fields.append(f"{key} = ?")
                    parameters.append(value)
            
            # 同時更新 updated_at 為當下時間
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            
            if not update_fields:
                return False
                
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
            parameters.append(task_id)
            
            cursor.execute(query, tuple(parameters))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"更新任務錯誤: {e}")
            return False

    @staticmethod
    def delete(task_id):
        """
        根據 ID 刪除單筆任務記錄。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"刪除任務錯誤: {e}")
            return False
