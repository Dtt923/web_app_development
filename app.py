from flask import Flask
from app.routes.task_routes import task_bp
import os

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 基礎設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 確保 instance 資料夾存在，用來存放 SQLite 資料庫
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 註冊 Blueprint
    app.register_blueprint(task_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
