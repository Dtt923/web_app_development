from flask import Blueprint, render_template, request, redirect, url_for, flash

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁，包含所有任務列表與新增任務的表單。
    可以透過 GET 參數篩選已完成/未完成的任務。
    """
    pass

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    接收新增任務的表單資料。
    驗證資料後呼叫 Model 存入資料庫，接著重導向回首頁。
    """
    pass

@task_bp.route('/tasks/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    顯示特定任務的編輯表單頁面。
    若任務不存在，則回傳 404 或重導向回首頁。
    """
    pass

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    接收編輯任務的表單資料。
    更新資料庫後重導向回首頁。
    """
    pass

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    將特定任務從資料庫中刪除。
    完成後重導向回首頁。
    """
    pass

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    改變特定任務的 `is_completed` 狀態。
    完成後重導向回首頁。
    """
    pass
