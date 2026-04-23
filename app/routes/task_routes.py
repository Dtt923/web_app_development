from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁，包含所有任務列表與新增任務的表單。
    可以透過 GET 參數篩選已完成/未完成的任務。
    """
    tasks = Task.get_all()
    
    # 處理過濾邏輯
    status_filter = request.args.get('status')
    if status_filter == 'completed':
        tasks = [t for t in tasks if t['is_completed'] == 1]
    elif status_filter == 'pending':
        tasks = [t for t in tasks if t['is_completed'] == 0]
        
    return render_template('index.html', tasks=tasks, current_filter=status_filter)

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    接收新增任務的表單資料。
    驗證資料後呼叫 Model 存入資料庫，接著重導向回首頁。
    """
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')

    # 基本的輸入驗證
    if not title or title.strip() == '':
        flash('標題為必填欄位', 'error')
        return redirect(url_for('task_bp.index'))

    data = {
        'title': title.strip(),
        'description': description.strip() if description else '',
        'due_date': due_date if due_date else None
    }
    
    success = Task.create(data)
    if success:
        flash('任務新增成功！', 'success')
    else:
        flash('新增任務失敗，請稍後再試。', 'error')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    顯示特定任務的編輯表單頁面。
    若任務不存在，則回傳 404 或重導向回首頁。
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務。', 'error')
        return redirect(url_for('task_bp.index'))
        
    return render_template('edit.html', task=task)

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    接收編輯任務的表單資料。
    更新資料庫後重導向回首頁。
    """
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')

    # 驗證
    if not title or title.strip() == '':
        flash('標題為必填欄位', 'error')
        return redirect(url_for('task_bp.edit_task', id=id))

    data = {
        'title': title.strip(),
        'description': description.strip() if description else '',
        'due_date': due_date if due_date else None
    }
    
    success = Task.update(id, data)
    if success:
        flash('任務更新成功！', 'success')
    else:
        flash('更新任務失敗，請稍後再試。', 'error')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    將特定任務從資料庫中刪除。
    完成後重導向回首頁。
    """
    success = Task.delete(id)
    if success:
        flash('任務已刪除。', 'success')
    else:
        flash('刪除任務失敗，請稍後再試。', 'error')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    改變特定任務的 `is_completed` 狀態。
    完成後重導向回首頁。
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務。', 'error')
        return redirect(url_for('task_bp.index'))
        
    new_status = 0 if task['is_completed'] else 1
    success = Task.update(id, {'is_completed': new_status})
    
    if not success:
        flash('更新狀態失敗，請稍後再試。', 'error')
        
    return redirect(url_for('task_bp.index'))
