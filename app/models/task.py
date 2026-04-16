import sqlite3
import os
from contextlib import closing

# 設定資料庫路徑 (對應架構文件設定的 instance/database.db)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

class Task:
    @staticmethod
    def get_connection():
        """獲取資料庫連接，並開啟 Row-factory 讓取出的資料可以轉作 dictionary 存取"""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, description, due_date):
        """新增一個任務"""
        with closing(cls.get_connection()) as conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO tasks (title, description, due_date)
                    VALUES (?, ?, ?)
                    ''',
                    (title, description, due_date)
                )
                return cursor.lastrowid

    @classmethod
    def get_all(cls):
        """取得所有任務清單"""
        with closing(cls.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            return cursor.fetchall()

    @classmethod
    def get_by_id(cls, task_id):
        """根據 ID 取得單一任務"""
        with closing(cls.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            return cursor.fetchone()

    @classmethod
    def update(cls, task_id, title, description, due_date):
        """更新任務的資訊"""
        with closing(cls.get_connection()) as conn:
            with conn:
                conn.execute(
                    '''
                    UPDATE tasks
                    SET title = ?, description = ?, due_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    ''',
                    (title, description, due_date, task_id)
                )
                
    @classmethod
    def toggle_status(cls, task_id):
        """切換任務的未完成/已完成狀態"""
        with closing(cls.get_connection()) as conn:
            with conn:
                conn.execute(
                    '''
                    UPDATE tasks
                    SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    ''',
                    (task_id,)
                )

    @classmethod
    def delete(cls, task_id):
        """刪除指定任務"""
        with closing(cls.get_connection()) as conn:
            with conn:
                conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
